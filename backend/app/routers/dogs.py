from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/dogs", tags=["dogs"])


@router.get("", response_model=schemas.DogListResponse)
def list_dogs(
    size: Optional[str] = Query(None),
    breed_group: Optional[str] = Query(None),
    min_energy: Optional[int] = Query(None, ge=1, le=5),
    max_energy: Optional[int] = Query(None, ge=1, le=5),
    min_friendliness: Optional[float] = Query(None, ge=1, le=5),
    kid_friendly: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Dog)
    if size:
        q = q.filter(models.Dog.size == size)
    if breed_group:
        q = q.filter(models.Dog.breed_group == breed_group)
    if min_energy is not None:
        q = q.filter(models.Dog.energy_level >= min_energy)
    if max_energy is not None:
        q = q.filter(models.Dog.energy_level <= max_energy)
    if min_friendliness is not None:
        q = q.filter(models.Dog.friendliness >= min_friendliness)
    if kid_friendly is not None:
        threshold = 3
        if kid_friendly:
            q = q.filter(models.Dog.kid_friendly >= threshold)
        else:
            q = q.filter(models.Dog.kid_friendly < threshold)
    total = q.count()
    items = q.order_by(models.Dog.breed_name).all()
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
