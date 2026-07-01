from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.agent import DogContext, answer_dog_question
from app.breed_enrichment import generate_and_store_embedding
from app.database import get_db
from app import models, schemas
from app.schemas import BreedGroup

router = APIRouter(prefix="/dogs", tags=["dogs"])


def _rating_query():
    """Default query param for a 1-5 rating filter bound (min or max)."""
    return Query(None, ge=1, le=5)


@router.get("", response_model=schemas.DogListResponse)
async def list_dogs(
    size: Optional[str] = Query(None),
    breed_group: Optional[BreedGroup] = Query(None),
    # Adaptability
    min_apartment_friendly: Optional[int] = _rating_query(),
    max_apartment_friendly: Optional[int] = _rating_query(),
    min_good_for_novice: Optional[int] = _rating_query(),
    max_good_for_novice: Optional[int] = _rating_query(),
    min_sensitivity: Optional[int] = _rating_query(),
    max_sensitivity: Optional[int] = _rating_query(),
    min_tolerates_alone: Optional[int] = _rating_query(),
    max_tolerates_alone: Optional[int] = _rating_query(),
    min_tolerates_cold: Optional[int] = _rating_query(),
    max_tolerates_cold: Optional[int] = _rating_query(),
    min_tolerates_hot: Optional[int] = _rating_query(),
    max_tolerates_hot: Optional[int] = _rating_query(),
    # Friendliness
    min_friendliness: Optional[int] = _rating_query(),
    max_friendliness: Optional[int] = _rating_query(),
    min_affectionate_family: Optional[int] = _rating_query(),
    max_affectionate_family: Optional[int] = _rating_query(),
    min_kid_friendly: Optional[int] = _rating_query(),
    max_kid_friendly: Optional[int] = _rating_query(),
    min_dog_friendly: Optional[int] = _rating_query(),
    max_dog_friendly: Optional[int] = _rating_query(),
    min_stranger_friendly: Optional[int] = _rating_query(),
    max_stranger_friendly: Optional[int] = _rating_query(),
    # Health & Grooming
    min_health_grooming: Optional[int] = _rating_query(),
    max_health_grooming: Optional[int] = _rating_query(),
    min_shedding: Optional[int] = _rating_query(),
    max_shedding: Optional[int] = _rating_query(),
    min_drooling: Optional[int] = _rating_query(),
    max_drooling: Optional[int] = _rating_query(),
    min_easy_groom: Optional[int] = _rating_query(),
    max_easy_groom: Optional[int] = _rating_query(),
    min_general_health: Optional[int] = _rating_query(),
    max_general_health: Optional[int] = _rating_query(),
    min_weight_gain_potential: Optional[int] = _rating_query(),
    max_weight_gain_potential: Optional[int] = _rating_query(),
    min_size_score: Optional[int] = _rating_query(),
    max_size_score: Optional[int] = _rating_query(),
    # Trainability
    min_trainability: Optional[int] = _rating_query(),
    max_trainability: Optional[int] = _rating_query(),
    min_easy_train: Optional[int] = _rating_query(),
    max_easy_train: Optional[int] = _rating_query(),
    min_intelligence: Optional[int] = _rating_query(),
    max_intelligence: Optional[int] = _rating_query(),
    min_mouthiness: Optional[int] = _rating_query(),
    max_mouthiness: Optional[int] = _rating_query(),
    min_prey_drive: Optional[int] = _rating_query(),
    max_prey_drive: Optional[int] = _rating_query(),
    min_barking: Optional[int] = _rating_query(),
    max_barking: Optional[int] = _rating_query(),
    min_wanderlust: Optional[int] = _rating_query(),
    max_wanderlust: Optional[int] = _rating_query(),
    # Physical Needs
    min_physical_needs: Optional[int] = _rating_query(),
    max_physical_needs: Optional[int] = _rating_query(),
    min_energy_level: Optional[int] = _rating_query(),
    max_energy_level: Optional[int] = _rating_query(),
    min_intensity: Optional[int] = _rating_query(),
    max_intensity: Optional[int] = _rating_query(),
    min_exercise_needs: Optional[int] = _rating_query(),
    max_exercise_needs: Optional[int] = _rating_query(),
    min_playfulness: Optional[int] = _rating_query(),
    max_playfulness: Optional[int] = _rating_query(),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.Dog)

    if size:
        stmt = stmt.where(models.Dog.size == size)
    if breed_group:
        stmt = stmt.where(models.Dog.breed_group == breed_group.value)

    range_filters = [
        (models.Dog.apartment_friendly, min_apartment_friendly, max_apartment_friendly),
        (models.Dog.good_for_novice, min_good_for_novice, max_good_for_novice),
        (models.Dog.sensitivity, min_sensitivity, max_sensitivity),
        (models.Dog.tolerates_alone, min_tolerates_alone, max_tolerates_alone),
        (models.Dog.tolerates_cold, min_tolerates_cold, max_tolerates_cold),
        (models.Dog.tolerates_hot, min_tolerates_hot, max_tolerates_hot),
        (models.Dog.friendliness, min_friendliness, max_friendliness),
        (
            models.Dog.affectionate_family,
            min_affectionate_family,
            max_affectionate_family,
        ),
        (models.Dog.kid_friendly, min_kid_friendly, max_kid_friendly),
        (models.Dog.dog_friendly, min_dog_friendly, max_dog_friendly),
        (models.Dog.stranger_friendly, min_stranger_friendly, max_stranger_friendly),
        (models.Dog.health_grooming, min_health_grooming, max_health_grooming),
        (models.Dog.shedding, min_shedding, max_shedding),
        (models.Dog.drooling, min_drooling, max_drooling),
        (models.Dog.easy_groom, min_easy_groom, max_easy_groom),
        (models.Dog.general_health, min_general_health, max_general_health),
        (
            models.Dog.weight_gain_potential,
            min_weight_gain_potential,
            max_weight_gain_potential,
        ),
        (models.Dog.size_score, min_size_score, max_size_score),
        (models.Dog.trainability, min_trainability, max_trainability),
        (models.Dog.easy_train, min_easy_train, max_easy_train),
        (models.Dog.intelligence, min_intelligence, max_intelligence),
        (models.Dog.mouthiness, min_mouthiness, max_mouthiness),
        (models.Dog.prey_drive, min_prey_drive, max_prey_drive),
        (models.Dog.barking, min_barking, max_barking),
        (models.Dog.wanderlust, min_wanderlust, max_wanderlust),
        (models.Dog.physical_needs, min_physical_needs, max_physical_needs),
        (models.Dog.energy_level, min_energy_level, max_energy_level),
        (models.Dog.intensity, min_intensity, max_intensity),
        (models.Dog.exercise_needs, min_exercise_needs, max_exercise_needs),
        (models.Dog.playfulness, min_playfulness, max_playfulness),
    ]

    for column, min_val, max_val in range_filters:
        if min_val is not None:
            stmt = stmt.where(column >= min_val)
        if max_val is not None:
            stmt = stmt.where(column <= max_val)

    SORTABLE = {
        "breed_name": models.Dog.breed_name,
        "energy_level": models.Dog.energy_level,
        "friendliness": models.Dog.friendliness,
        "trainability": models.Dog.trainability,
        "adaptability": models.Dog.adaptability,
        "intelligence": models.Dog.intelligence,
        "kid_friendly": models.Dog.kid_friendly,
        "playfulness": models.Dog.playfulness,
    }
    sort_col = SORTABLE.get(sort_by, models.Dog.breed_name)
    total = await db.scalar(select(func.count()).select_from(stmt.subquery()))
    stmt = stmt.order_by(sort_col.desc() if sort_order == "desc" else sort_col.asc())
    result = await db.execute(stmt)
    items = result.scalars().all()
    return {"total": total, "items": items}


@router.get("/{dog_id}", response_model=schemas.DogOut)
async def get_dog(dog_id: int, db: AsyncSession = Depends(get_db)):
    dog = await db.get(models.Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog


@router.post("", response_model=schemas.DogOut, status_code=201)
async def create_dog(
    dog_in: schemas.DogCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    existing = await db.scalar(
        select(models.Dog).where(models.Dog.breed_name == dog_in.breed_name)
    )
    if existing:
        raise HTTPException(status_code=409, detail="Breed already exists")
    dog = models.Dog(**dog_in.model_dump())
    db.add(dog)
    await db.commit()
    await db.refresh(dog)
    background_tasks.add_task(generate_and_store_embedding, dog.id)
    return dog


@router.get("/{dog_id}/embedding")
async def get_dog_embedding(dog_id: int, db: AsyncSession = Depends(get_db)):
    dog = await db.get(models.Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    return {
        "id": dog.id,
        "breed_name": dog.breed_name,
        "owner_summary": dog.owner_summary,
        "embedding": dog.embedding.tolist() if dog.embedding is not None else None,
    }


@router.delete("/{dog_id}", status_code=204)
async def delete_dog(dog_id: int, db: AsyncSession = Depends(get_db)):
    dog = await db.get(models.Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    await db.delete(dog)
    await db.commit()


@router.post("/{dog_id}/chat", response_model=schemas.ChatResponse)
async def chat_about_dog(
    dog_id: int,
    body: schemas.ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> schemas.ChatResponse:
    dog = await db.get(models.Dog, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    context = DogContext(
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
        easy_groom=dog.easy_groom,
        general_health=dog.general_health,
        trainability=dog.trainability,
        easy_train=dog.easy_train,
        intelligence=dog.intelligence,
        barking=dog.barking,
        energy_level=dog.energy_level,
        exercise_needs=dog.exercise_needs,
        playfulness=dog.playfulness,
        description=dog.description,
    )
    answer, session_id = await answer_dog_question(
        context, body.question, body.session_id
    )
    return schemas.ChatResponse(answer=answer, session_id=session_id)
