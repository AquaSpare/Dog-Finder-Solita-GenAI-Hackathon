"""Seed the database by POSTing breeds to the running API.

Reads the scraped CSV and creates each breed via ``POST /dogs`` on the running
backend (default http://localhost:8000, override with ``API_BASE_URL``).

Re-runnable: the create endpoint returns 409 for a breed that already exists, so
those rows are simply skipped. The API has no update endpoint, so existing rows
are not refreshed — drop them first (or reset the database) if you need to reload.
"""

import os
import sys

import httpx
import polars as pl
from tqdm import tqdm

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../scraping/assets/dogs_cleaned_with_description_and_img.csv",
)

COLUMN_MAP = {
    "Breed Name": "breed_name",
    "Dog Size": "size",
    "Dog Breed Group": "breed_group",
    "Height": "height",
    "Avg. Height, cm": "avg_height_cm",
    "Weight": "weight",
    "Avg. Weight, kg": "avg_weight_kg",
    "Life Span": "life_span",
    "Avg. Life Span, years": "avg_life_span_years",
    "Adaptability": "adaptability",
    "Adapts Well To Apartment Living": "apartment_friendly",
    "Good For Novice Owners": "good_for_novice",
    "Sensitivity Level": "sensitivity",
    "Tolerates Being Alone": "tolerates_alone",
    "Tolerates Cold Weather": "tolerates_cold",
    "Tolerates Hot Weather": "tolerates_hot",
    "All Around Friendliness": "friendliness",
    "Affectionate With Family": "affectionate_family",
    "Kid-Friendly": "kid_friendly",
    "Dog Friendly": "dog_friendly",
    "Friendly Toward Strangers": "stranger_friendly",
    "Health And Grooming Needs": "health_grooming",
    "Amount Of Shedding": "shedding",
    "Drooling Potential": "drooling",
    "Easy To Groom": "easy_groom",
    "General Health": "general_health",
    "Potential For Weight Gain": "weight_gain_potential",
    "Size": "size_score",
    "Trainability": "trainability",
    "Easy To Train": "easy_train",
    "Intelligence": "intelligence",
    "Potential For Mouthiness": "mouthiness",
    "Prey Drive": "prey_drive",
    "Tendency To Bark Or Howl": "barking",
    "Wanderlust Potential": "wanderlust",
    "Physical Needs": "physical_needs",
    "Energy Level": "energy_level",
    "Intensity": "intensity",
    "Exercise Needs": "exercise_needs",
    "Potential For Playfulness": "playfulness",
    "Description": "description",
    "Image URL": "image_url",
}

INT_FIELDS = {
    "apartment_friendly",
    "good_for_novice",
    "sensitivity",
    "tolerates_alone",
    "tolerates_cold",
    "tolerates_hot",
    "affectionate_family",
    "kid_friendly",
    "dog_friendly",
    "stranger_friendly",
    "shedding",
    "easy_groom",
    "general_health",
    "weight_gain_potential",
    "size_score",
    "easy_train",
    "intelligence",
    "mouthiness",
    "wanderlust",
    "energy_level",
    "intensity",
    "exercise_needs",
    "playfulness",
}


def _coerce(field: str, value):
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    if field in INT_FIELDS:
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None
    return value


def main():
    df = pl.read_csv(CSV_PATH, infer_schema_length=0)
    df = df.rename({c: COLUMN_MAP[c] for c in df.columns if c in COLUMN_MAP})

    created = 0
    skipped = 0
    failed = 0

    with httpx.Client(base_url=API_BASE_URL, timeout=30.0) as client:
        try:
            client.get("/health").raise_for_status()
        except httpx.HTTPError as exc:
            sys.exit(
                f"API not reachable at {API_BASE_URL} ({exc}). Start the backend first."
            )

        for row in tqdm(df.iter_rows(named=True), total=df.height, desc="Seeding"):
            payload = {
                field: _coerce(field, row.get(field))
                for field in COLUMN_MAP.values()
                if field in row
            }
            resp = client.post("/dogs", json=payload)
            if resp.status_code == 201:
                created += 1
            elif resp.status_code == 409:
                skipped += 1
            else:
                failed += 1
                tqdm.write(
                    f"  {payload.get('breed_name')}: {resp.status_code} {resp.text[:200]}"
                )

    print(
        f"Done: {created} created, {skipped} skipped (already existed), {failed} failed"
    )
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
