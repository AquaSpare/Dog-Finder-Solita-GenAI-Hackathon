import asyncio
import logging

from sqlalchemy import update

from app import models
from app.database import SessionLocal
from app.embeddings import embed_text
from app.summarizer import BreedFacts, summarize_breed

logger = logging.getLogger("app.breed_enrichment")

_azure_semaphore = asyncio.Semaphore(4)


def _facts_from_dog(dog: models.Dog) -> BreedFacts:
    return BreedFacts(
        breed_name=dog.breed_name,
        size=dog.size,
        breed_group=dog.breed_group,
        height=dog.height,
        weight=dog.weight,
        life_span=dog.life_span,
        adaptability=dog.adaptability,
        apartment_friendly=dog.apartment_friendly,
        good_for_novice=dog.good_for_novice,
        sensitivity=dog.sensitivity,
        tolerates_alone=dog.tolerates_alone,
        tolerates_cold=dog.tolerates_cold,
        tolerates_hot=dog.tolerates_hot,
        friendliness=dog.friendliness,
        affectionate_family=dog.affectionate_family,
        kid_friendly=dog.kid_friendly,
        dog_friendly=dog.dog_friendly,
        stranger_friendly=dog.stranger_friendly,
        shedding=dog.shedding,
        drooling=dog.drooling,
        easy_groom=dog.easy_groom,
        general_health=dog.general_health,
        trainability=dog.trainability,
        easy_train=dog.easy_train,
        intelligence=dog.intelligence,
        mouthiness=dog.mouthiness,
        prey_drive=dog.prey_drive,
        barking=dog.barking,
        wanderlust=dog.wanderlust,
        energy_level=dog.energy_level,
        intensity=dog.intensity,
        exercise_needs=dog.exercise_needs,
        playfulness=dog.playfulness,
        description=dog.description,
    )


async def generate_and_store_embedding(dog_id: int) -> None:
    try:
        async with SessionLocal() as db:
            dog = await db.get(models.Dog, dog_id)
            if dog is None:
                logger.warning("Dog %s vanished before enrichment could run", dog_id)
                return
            facts = _facts_from_dog(dog)

            async with _azure_semaphore:
                summary = await summarize_breed(facts)
                embedding = await embed_text(summary)

            await db.execute(
                update(models.Dog)
                .where(models.Dog.id == dog_id)
                .values(owner_summary=summary, embedding=embedding)
            )
            await db.commit()
            logger.info("Enriched breed %s (id=%s)", dog.breed_name, dog_id)
    except Exception:
        logger.exception("Failed to enrich breed id=%s", dog_id)
