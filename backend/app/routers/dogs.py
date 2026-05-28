from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.agent import DogContext, answer_dog_question
from app.database import get_db
from app import models, schemas
from app.schemas import BreedGroup

router = APIRouter(prefix="/dogs", tags=["dogs"])

_I = lambda: Query(None, ge=1, le=5)


@router.get("", response_model=schemas.DogListResponse)
def list_dogs(
    size: Optional[str] = Query(None),
    breed_group: Optional[BreedGroup] = Query(None),
    # Adaptability
    min_apartment_friendly: Optional[int] = _I(),
    max_apartment_friendly: Optional[int] = _I(),
    min_good_for_novice: Optional[int] = _I(),
    max_good_for_novice: Optional[int] = _I(),
    min_sensitivity: Optional[int] = _I(),
    max_sensitivity: Optional[int] = _I(),
    min_tolerates_alone: Optional[int] = _I(),
    max_tolerates_alone: Optional[int] = _I(),
    min_tolerates_cold: Optional[int] = _I(),
    max_tolerates_cold: Optional[int] = _I(),
    min_tolerates_hot: Optional[int] = _I(),
    max_tolerates_hot: Optional[int] = _I(),
    # Friendliness
    min_friendliness: Optional[int] = _I(),
    max_friendliness: Optional[int] = _I(),
    min_affectionate_family: Optional[int] = _I(),
    max_affectionate_family: Optional[int] = _I(),
    min_kid_friendly: Optional[int] = _I(),
    max_kid_friendly: Optional[int] = _I(),
    min_dog_friendly: Optional[int] = _I(),
    max_dog_friendly: Optional[int] = _I(),
    min_stranger_friendly: Optional[int] = _I(),
    max_stranger_friendly: Optional[int] = _I(),
    # Health & Grooming
    min_health_grooming: Optional[int] = _I(),
    max_health_grooming: Optional[int] = _I(),
    min_shedding: Optional[int] = _I(),
    max_shedding: Optional[int] = _I(),
    min_drooling: Optional[int] = _I(),
    max_drooling: Optional[int] = _I(),
    min_easy_groom: Optional[int] = _I(),
    max_easy_groom: Optional[int] = _I(),
    min_general_health: Optional[int] = _I(),
    max_general_health: Optional[int] = _I(),
    min_weight_gain_potential: Optional[int] = _I(),
    max_weight_gain_potential: Optional[int] = _I(),
    min_size_score: Optional[int] = _I(),
    max_size_score: Optional[int] = _I(),
    # Trainability
    min_trainability: Optional[int] = _I(),
    max_trainability: Optional[int] = _I(),
    min_easy_train: Optional[int] = _I(),
    max_easy_train: Optional[int] = _I(),
    min_intelligence: Optional[int] = _I(),
    max_intelligence: Optional[int] = _I(),
    min_mouthiness: Optional[int] = _I(),
    max_mouthiness: Optional[int] = _I(),
    min_prey_drive: Optional[int] = _I(),
    max_prey_drive: Optional[int] = _I(),
    min_barking: Optional[int] = _I(),
    max_barking: Optional[int] = _I(),
    min_wanderlust: Optional[int] = _I(),
    max_wanderlust: Optional[int] = _I(),
    # Physical Needs
    min_physical_needs: Optional[int] = _I(),
    max_physical_needs: Optional[int] = _I(),
    min_energy_level: Optional[int] = _I(),
    max_energy_level: Optional[int] = _I(),
    min_intensity: Optional[int] = _I(),
    max_intensity: Optional[int] = _I(),
    min_exercise_needs: Optional[int] = _I(),
    max_exercise_needs: Optional[int] = _I(),
    min_playfulness: Optional[int] = _I(),
    max_playfulness: Optional[int] = _I(),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc"),
    db: Session = Depends(get_db),
):
    q = db.query(models.Dog)

    if size:
        q = q.filter(models.Dog.size == size)
    if breed_group:
        q = q.filter(models.Dog.breed_group == breed_group.value)

    range_filters = [
        (models.Dog.apartment_friendly, min_apartment_friendly, max_apartment_friendly),
        (models.Dog.good_for_novice, min_good_for_novice, max_good_for_novice),
        (models.Dog.sensitivity, min_sensitivity, max_sensitivity),
        (models.Dog.tolerates_alone, min_tolerates_alone, max_tolerates_alone),
        (models.Dog.tolerates_cold, min_tolerates_cold, max_tolerates_cold),
        (models.Dog.tolerates_hot, min_tolerates_hot, max_tolerates_hot),
        (models.Dog.friendliness, min_friendliness, max_friendliness),
        (models.Dog.affectionate_family, min_affectionate_family, max_affectionate_family),
        (models.Dog.kid_friendly, min_kid_friendly, max_kid_friendly),
        (models.Dog.dog_friendly, min_dog_friendly, max_dog_friendly),
        (models.Dog.stranger_friendly, min_stranger_friendly, max_stranger_friendly),
        (models.Dog.health_grooming, min_health_grooming, max_health_grooming),
        (models.Dog.shedding, min_shedding, max_shedding),
        (models.Dog.drooling, min_drooling, max_drooling),
        (models.Dog.easy_groom, min_easy_groom, max_easy_groom),
        (models.Dog.general_health, min_general_health, max_general_health),
        (models.Dog.weight_gain_potential, min_weight_gain_potential, max_weight_gain_potential),
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
            q = q.filter(column >= min_val)
        if max_val is not None:
            q = q.filter(column <= max_val)

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
    total = q.count()
    items = q.order_by(sort_col.desc() if sort_order == "desc" else sort_col.asc()).all()
    return {"total": total, "items": items}


@router.get("/{dog_id}", response_model=schemas.DogOut)
def get_dog(dog_id: int, db: Session = Depends(get_db)):
    dog = db.query(models.Dog).filter(models.Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog


@router.post("", response_model=schemas.DogOut, status_code=201)
def create_dog(dog_in: schemas.DogCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Dog).filter(models.Dog.breed_name == dog_in.breed_name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Breed already exists")
    dog = models.Dog(**dog_in.model_dump())
    db.add(dog)
    db.commit()
    db.refresh(dog)
    return dog


@router.delete("/{dog_id}", status_code=204)
def delete_dog(dog_id: int, db: Session = Depends(get_db)):
    dog = db.query(models.Dog).filter(models.Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    db.delete(dog)
    db.commit()


@router.post("/{dog_id}/chat", response_model=schemas.ChatResponse)
async def chat_about_dog(
    dog_id: int,
    body: schemas.ChatRequest,
    db: Session = Depends(get_db),
) -> schemas.ChatResponse:
    dog = db.query(models.Dog).filter(models.Dog.id == dog_id).first()
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
    answer, session_id = await answer_dog_question(context, body.question, body.session_id)
    return schemas.ChatResponse(answer=answer, session_id=session_id)
