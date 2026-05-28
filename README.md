# Dog Finder

A dog breed explorer with an AI chat assistant. Built as a submission for the **Solita Gen AI Hackathon** — fully designed and implemented in under 3 hours.

Browse 391 dog breeds, filter by traits, and ask an AI anything about a specific breed.

## Data

The breed data originates from a [Kaggle dataset](https://www.kaggle.com/datasets/yonkotoshiro/dogs-breeds/data?select=dogs_cleaned.csv) covering 391 breeds with trait scores. Each breed entry in the dataset included a link to its breed page, which was then scraped using Scrapy to pull richer descriptions and images — giving the app a more complete profile per breed. The processed data is loaded into SQLite via a seed script (`backend/app/seed.py`).

## What it does

- Browse and search a database of 391 dog breeds with detailed trait scores (friendliness, energy, trainability, etc.)
- View breed profiles including size, life span, and compatibility ratings
- Chat with an AI assistant about any breed — powered by GPT-4.1-mini via Azure OpenAI, with per-session conversation memory

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 19, Vite, Tailwind CSS |
| Backend | FastAPI, SQLAlchemy, SQLite |
| AI agent | Pydantic AI, GPT-4.1-mini (Azure OpenAI) |
| Data | Kaggle dataset + Scrapy scraper → seeded via `seed.py` |

## Structure

```
├── frontend/   # React app
├── backend/    # FastAPI + AI agent
└── scraping/   # Scrapy scraper & raw data
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
