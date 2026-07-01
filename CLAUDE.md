# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common commands

The whole stack is orchestrated by the top-level `docker-compose.yml` (Postgres + FastAPI backend + Vite frontend). The seed script and any `python -m app.*` calls target the *running* backend container.

```bash
# Full stack (Postgres, backend, frontend)
docker compose up --build

# Seed the 391-breed dataset by POSTing to the running API. Safe to re-run
# (existing breeds return 409 and are skipped). Enrichment (summary +
# embedding) is scheduled as a FastAPI BackgroundTask, so rows finish
# populating a few seconds after the POST returns.
docker compose exec backend python -m app.seed
docker compose exec backend python -m app.seed --limit 5   # partial reload while iterating on prompts

# Watch enrichment progress
docker compose exec db psql -U dogs -d dogs_db -c \
  "SELECT COUNT(*) FILTER (WHERE embedding IS NULL) AS pending, COUNT(*) AS total FROM dogs;"
```

Backend (run inside `backend/`, uses `uv`):

```bash
uv sync                                      # install deps
uv run uvicorn app.main:app --reload         # run locally against DATABASE_URL (default localhost:5432)
uv run ruff check .                          # lint
uv run ruff format .                         # format
```

Frontend (run inside `frontend/`):

```bash
npm install
npm run dev        # Vite dev server on :5173
npm run build
npm run lint       # eslint
```

There is no test suite in this repo.

## Architecture

### Three top-level dirs
- `backend/` — FastAPI async app (Python 3.13, SQLAlchemy async, pgvector).
- `frontend/` — React 19 + Vite + Tailwind v4 SPA.
- `scraping/` — Scrapy notebook + the cleaned CSV that `app/seed.py` reads.

### Backend layout (`backend/app/`)
- `main.py` — FastAPI entry. **Calls `load_dotenv()` before importing any app modules on purpose** — `database.py` and the routers read env vars at import time. The `E402` ruff exception is configured for this file in `pyproject.toml`; keep that ordering. The lifespan enables the `vector` extension and runs `Base.metadata.create_all` — there is no Alembic migration flow wired up despite alembic being a dependency.
- `database.py` — Async engine + `SessionLocal`; `get_db()` yields a session for FastAPI DI.
- `models.py` — Single `Dog` SQLAlchemy model. `embedding` is a `pgvector` `Vector(EMBEDDING_DIM)` column whose dimension is fixed at table-create time from `AZURE_OPENAI_EMBEDDING_DIMENSIONS` (default 1536). Changing that env var on an existing DB will not resize the column — you must drop the table.
- `routers/dogs.py` — All HTTP routes live under `/dogs`. `GET /dogs` accepts a large flat set of `min_*` / `max_*` rating filters (1–5) plus `size`, `breed_group`, `sort_by`, `sort_order`. `POST /dogs` schedules `generate_and_store_embedding` as a `BackgroundTasks` callback. `POST /dogs/{id}/chat` proxies to the Pydantic AI chat agent.
- `schemas.py` — Pydantic request/response models + the `BreedGroup` enum used for filter validation.
- `agent.py` — The `chat_agent` (Pydantic AI `Agent`). Uses `OpenAIChatModel` + `AzureProvider`. Session memory is a **process-local `dict[str, list[ModelMessage]]`** keyed by `session_id`; it does not survive restarts and is not shared across workers. Wraps runs in `asyncio.wait_for(..., timeout=15.0)` and maps failures to `504` / `502`.
- `summarizer.py` — Lower-temp (`0.1`) Pydantic AI agent that turns a `BreedFacts` record into a first-person, ~90–130 word paragraph from a *prospective owner's* perspective. Never names the breed and never restates column names — that constraint is enforced by both the system prompt (`prompts/breed_summary_prompt.md`) and the injected `@summarizer_agent.instructions`. Keep both in sync when editing.
- `embeddings.py` — Thin Pydantic AI `Embedder` wrapper around Azure OpenAI's embedding deployment.
- `breed_enrichment.py` — Background task run on every `POST /dogs`. Loads the row → summarizes → embeds → writes both `owner_summary` and `embedding` back. Concurrent Azure calls are capped by a module-level `asyncio.Semaphore(4)` — respect this when adding new AI calls that also hit Azure.
- `seed.py` — Loads `scraping/assets/dogs_cleaned_with_description_and_img.csv` with polars, maps CSV headers via `COLUMN_MAP`, then **POSTs each row to the running API** (does not write to the DB directly). This means the backend must already be up before seeding, and enrichment happens naturally via the create endpoint's background task.
- `prompts/` — Markdown system prompts. Loaded at import time via `Path(__file__).parent.parent / "prompts"`.

### Two Pydantic AI agents, both Azure-backed
Both `chat_agent` and `summarizer_agent` construct their model from the same env vars (`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`), but the summarizer uses its own deployment (`AZURE_OPENAI_SUMMARIZER_MODEL`) and the chat agent's model name is currently **hardcoded to `"gpt-5.4-mini"`** in `agent.py:66`. If you switch chat models, change it there.

### Frontend
- `src/api/dogs.js` — Single API client. `VITE_API_URL` overrides the default `http://localhost:8000`. `buildQuery` translates the UI's filter state (`{ breedGroups, sizes, ranges }`) into the flat `min_*`/`max_*` query params the backend expects; keep this mapping in sync with `routers/dogs.py` when adding a new rating filter.
- `src/pages/` — `HomePage` (list + filters) and `DogDetailPage` (profile + chat panel).
- `src/components/` — `home/`, `detail/`, `filters/`, `shared/` — self-explanatory groupings.
- Chat session continuity is client-driven: the first `POST /dogs/{id}/chat` returns a `session_id`; the frontend sends it back on subsequent messages so the backend's in-memory history dict picks up the same conversation.

### Data flow for a new breed
1. Client (or `seed.py`) → `POST /dogs` → row committed.
2. FastAPI `BackgroundTasks` triggers `generate_and_store_embedding(dog.id)`.
3. `summarize_breed` (Azure chat) → first-person owner paragraph.
4. `embed_text` (Azure embeddings) → vector.
5. Both written back to the same row. `GET /dogs/{id}/embedding` exposes the raw vector for debugging.

## Environment

Backend requires an Azure OpenAI resource. Copy `backend/.env.example` to `backend/.env` and fill in:
- `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`, `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_SUMMARIZER_MODEL` (chat deployment for the summarizer)
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` and `AZURE_OPENAI_EMBEDDING_DIMENSIONS` (must match the deployed model — 1536 for `text-embedding-3-small`, 3072 for `-large`)
- `DATABASE_URL` — inside compose this is `postgresql+psycopg://dogs:dogs@db:5432/dogs_db`; swap `db` → `localhost` when running the backend on the host against the Compose-managed database.
