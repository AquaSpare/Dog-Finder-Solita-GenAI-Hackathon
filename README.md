# Dog Finder

A **personal fullstack + RAG project** — an AI-powered dog breed explorer. The initial version was sparked at the **Solita Gen AI Hackathon**; it is now being developed further as a playground for fullstack, agent, and retrieval work.

Browse 391 dog breeds, filter by traits, and chat with an AI assistant that retrieves and reasons over real breed data using **Retrieval-Augmented Generation (RAG)**.

## Architecture

Dog Finder is a complete fullstack application with a clear separation between a modern React frontend and a Python API backend, connected through a well-defined REST interface.

```
┌─────────────────────────────┐     REST API     ┌──────────────────────────────────┐
│   Frontend (React + Vite)   │ ◄──────────────► │   Backend (FastAPI + SQLAlchemy) │
│   Tailwind CSS, React 19    │                  │   PostgreSQL, Pydantic AI        │
└─────────────────────────────┘                  └───────────────┬──────────────────┘
                                                                  │ RAG
                                                                  ▼
                                                   ┌─────────────────────────┐
                                                   │  Azure OpenAI / GPT     │
                                                   │  + breed context docs   │
                                                   └─────────────────────────┘
```

## RAG — Retrieval-Augmented Generation

The AI chat assistant does not rely on the model's base knowledge alone. When you ask about a breed, the backend **retrieves the breed's full structured profile** from the database — traits, size, temperament, life span, descriptions scraped from official breed pages — and injects it as grounding context into the prompt. This means:

- Answers are **anchored to real, sourced data** rather than model hallucinations
- The model can reason over 391 breeds with accurate, breed-specific detail
- Per-session conversation memory allows follow-up questions without losing context

## Frontend

Built with **React 19**, **Vite**, and **Tailwind CSS** for a fast, responsive, and modern UI:

- Instant breed search and multi-trait filtering
- Breed profile cards with images, scores, and compatibility ratings
- Embedded chat panel per breed — context switches automatically as you navigate

## Backend

A **FastAPI** REST API with **SQLAlchemy** and **PostgreSQL**:

- `/breeds` — paginated, searchable, filterable breed listing
- `/breeds/{id}` — full breed profile
- `/breeds/{id}/chat` — stateful AI chat endpoint backed by Pydantic AI and Azure OpenAI

The AI agent layer uses **Pydantic AI** to structure tool calls and enforce typed responses, keeping the LLM interaction predictable and testable.

### AI enrichment pipeline

Each breed is stored not just as structured columns but also as a dense vector, ready for semantic retrieval. When a breed is created via `POST /dogs`, a background task runs:

1. A low-temperature **Pydantic AI summarizer agent** turns the breed's structured data into a short, first-person paragraph written from a *prospective owner's* perspective — never naming the breed, never restating column names.
2. A **Pydantic AI embedder** (Azure OpenAI `text-embedding-3-small` by default) embeds that summary.
3. Both the summary and the vector are written back to the row (`owner_summary`, `embedding`).

The summary is exposed on `GET /dogs/{id}`; the raw vector is available on the debug endpoint `GET /dogs/{id}/embedding`. Similarity-search on top of these embeddings is the next step.

**PostgreSQL** with [`pgvector`](https://github.com/pgvector/pgvector) stores the embeddings as a native `vector(N)` column. The Docker Compose stack uses the `pgvector/pgvector:pg16` image; the extension is enabled automatically on backend startup. The database URL is configurable via the `DATABASE_URL` environment variable.

## Data

Full credit for the breed dataset used to seed this project goes to **[yonkotoshiro's Dogs Breeds dataset on Kaggle](https://www.kaggle.com/datasets/yonkotoshiro/dogs-breeds)** — 391 breeds with rich trait scores. Each breed entry included a link to its breed page, which was scraped with **Scrapy** to pull richer descriptions and images. The processed data is loaded into PostgreSQL via `backend/app/seed.py`.

The dataset is only what happens to be seeded — nothing about the app is coupled to it. The API accepts any dog you `POST /dogs`, and the enrichment pipeline (summary + embedding) runs on it automatically. Bring your own breeds, mutts, or made-up dogs.

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 19, Vite, Tailwind CSS |
| Backend | FastAPI, SQLAlchemy, PostgreSQL |
| AI / RAG | Pydantic AI, GPT (Azure OpenAI), structured breed retrieval |
| Data pipeline | Kaggle dataset + Scrapy scraper → seeded via `seed.py` |

## Structure

```
├── frontend/   # React 19 + Vite app (UI, routing, chat panel)
├── backend/    # FastAPI REST API + Pydantic AI RAG agent
└── scraping/   # Scrapy scraper & raw breed data
```

## Running locally

### With Docker (recommended)

The whole stack — PostgreSQL, the FastAPI backend, and the Vite frontend — runs from a single
`docker-compose.yml`.

```bash
# 1. Configure backend env (Azure OpenAI credentials power both the chat agent
#    and the summariser/embedder used for enrichment)
cp backend/.env.example backend/.env   # then fill in your Azure OpenAI values
```

The backend needs these Azure OpenAI values in `backend/.env`:

- `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_VERSION` — your Foundry resource
- `AZURE_OPENAI_API_KEY` — auth
- `AZURE_OPENAI_SUMMARIZER_MODEL` — chat deployment used by the summariser agent
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` — embedding deployment
- `AZURE_OPENAI_EMBEDDING_DIMENSIONS` — must match the deployed embedding model (1536 for `text-embedding-3-small`, 3072 for `-large`); pins the `vector(N)` column width at table-create time

```bash
# 2. Build and start everything
docker compose up --build

# 3. Seed the 391 breeds (POSTs each breed to the running API; safe to re-run —
#    breeds that already exist are skipped). Use --limit N for a cheap partial
#    reload while iterating on prompts.
docker compose exec backend python -m app.seed
docker compose exec backend python -m app.seed --limit 5   # just the first 5
```

The seed script populates the database by calling the API rather than writing to it directly,
so the backend must be running first (step 2 above). It targets `http://localhost:8000` by
default — override with the `API_BASE_URL` environment variable.

Each `POST /dogs` schedules enrichment as a **background task**, so the seed script returns
quickly but `owner_summary` and `embedding` populate a few seconds later per row. Watch
progress with:

```bash
docker compose exec db psql -U dogs -d dogs_db -c \
  "SELECT COUNT(*) FILTER (WHERE embedding IS NULL) AS pending, COUNT(*) AS total FROM dogs;"
```

- Frontend: http://localhost:5173
- API: http://localhost:8000 (health check at `/health`)
- Postgres data persists in the `pgdata` volume across `docker compose down` / `up`.

### Without Docker

Run just Postgres in Docker and the app on your host:

```bash
# Start only the database
docker compose up db

# Backend
cd backend
cp .env.example .env   # fill in Azure creds, and set DATABASE_URL host to localhost
# DATABASE_URL=postgresql+psycopg://dogs:dogs@localhost:5432/dogs_db
uv sync
uv run uvicorn app.main:app --reload

# Seed once, with the backend running, from another terminal
cd backend
uv run python app/seed.py

# Frontend (in a separate terminal)
cd frontend
npm install
npm run dev
```
