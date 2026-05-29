# Dog Finder

A **fullstack AI-powered dog breed explorer** built for the **Solita Gen AI Hackathon** — fully designed and implemented in under 3 hours.

Browse 391 dog breeds, filter by traits, and chat with an AI assistant that retrieves and reasons over real breed data using **Retrieval-Augmented Generation (RAG)**.

## Architecture

Dog Finder is a complete fullstack application with a clear separation between a modern React frontend and a Python API backend, connected through a well-defined REST interface.

```
┌─────────────────────────────┐     REST API     ┌──────────────────────────────────┐
│   Frontend (React + Vite)   │ ◄──────────────► │   Backend (FastAPI + SQLAlchemy) │
│   Tailwind CSS, React 19    │                  │   SQLite, Pydantic AI            │
└─────────────────────────────┘                  └───────────────┬──────────────────┘
                                                                  │ RAG
                                                                  ▼
                                                   ┌─────────────────────────┐
                                                   │  Azure OpenAI / GPT-4.1 │
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

A **FastAPI** REST API with **SQLAlchemy** and SQLite:

- `/breeds` — paginated, searchable, filterable breed listing
- `/breeds/{id}` — full breed profile
- `/breeds/{id}/chat` — stateful AI chat endpoint backed by Pydantic AI and Azure OpenAI

The AI agent layer uses **Pydantic AI** to structure tool calls and enforce typed responses, keeping the LLM interaction predictable and testable.

## Data

The breed data originates from a [Kaggle dataset](https://www.kaggle.com/datasets/yonkotoshiro/dogs-breeds/data?select=dogs_cleaned.csv) covering 391 breeds with trait scores. Each breed entry included a link to its breed page, which was scraped with **Scrapy** to pull richer descriptions and images. The processed data is loaded into SQLite via `backend/app/seed.py`.

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 19, Vite, Tailwind CSS |
| Backend | FastAPI, SQLAlchemy, SQLite |
| AI / RAG | Pydantic AI, GPT-4.1-mini (Azure OpenAI), structured breed retrieval |
| Data pipeline | Kaggle dataset + Scrapy scraper → seeded via `seed.py` |

## Structure

```
├── frontend/   # React 19 + Vite app (UI, routing, chat panel)
├── backend/    # FastAPI REST API + Pydantic AI RAG agent
└── scraping/   # Scrapy scraper & raw breed data
```

## Running locally

**Backend**
```bash
cd backend
uv sync
cp .env.example .env  # fill in Azure OpenAI credentials
uv run uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```
