"""Seed the database from the scraped CSV. Safe to re-run (upserts by breed_name)."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import polars as pl
from app.database import SessionLocal, engine
from app import models
from app.database import Base

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
    "apartment_friendly", "good_for_novice", "sensitivity", "tolerates_alone",
    "tolerates_cold", "tolerates_hot", "affectionate_family", "kid_friendly",
    "dog_friendly", "stranger_friendly", "shedding", "easy_groom", "general_health",
    "weight_gain_potential", "size_score", "easy_train", "intelligence",
    "mouthiness", "wanderlust", "energy_level", "intensity", "exercise_needs",
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
    Base.metadata.create_all(bind=engine)

    df = pl.read_csv(CSV_PATH, infer_schema_length=0)
    df = df.rename({c: COLUMN_MAP[c] for c in df.columns if c in COLUMN_MAP})

    db = SessionLocal()
    seeded = 0
    updated = 0

    try:
        for row in df.iter_rows(named=True):
            data = {
                field: _coerce(field, row.get(field))
                for field in COLUMN_MAP.values()
                if field in row
            }
            existing = db.query(models.Dog).filter_by(breed_name=data["breed_name"]).first()
            if existing:
                for k, v in data.items():
                    setattr(existing, k, v)
                updated += 1
            else:
                db.add(models.Dog(**data))
                seeded += 1

        db.commit()
        print(f"Done: {seeded} inserted, {updated} updated ({seeded + updated} total breeds)")
    finally:
        db.close()


if __name__ == "__main__":
    main()
