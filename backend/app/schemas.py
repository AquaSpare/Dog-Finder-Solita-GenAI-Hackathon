from pydantic import BaseModel
from typing import Optional


class DogBase(BaseModel):
    breed_name: str
    size: Optional[str] = None
    breed_group: Optional[str] = None
    height: Optional[str] = None
    avg_height_cm: Optional[float] = None
    weight: Optional[str] = None
    avg_weight_kg: Optional[float] = None
    life_span: Optional[str] = None
    avg_life_span_years: Optional[float] = None
    adaptability: Optional[float] = None
    apartment_friendly: Optional[int] = None
    good_for_novice: Optional[int] = None
    sensitivity: Optional[int] = None
    tolerates_alone: Optional[int] = None
    tolerates_cold: Optional[int] = None
    tolerates_hot: Optional[int] = None
    friendliness: Optional[float] = None
    affectionate_family: Optional[int] = None
    kid_friendly: Optional[int] = None
    dog_friendly: Optional[int] = None
    stranger_friendly: Optional[int] = None
    health_grooming: Optional[float] = None
    shedding: Optional[int] = None
    drooling: Optional[float] = None
    easy_groom: Optional[int] = None
    general_health: Optional[int] = None
    weight_gain_potential: Optional[int] = None
    size_score: Optional[int] = None
    trainability: Optional[float] = None
    easy_train: Optional[int] = None
    intelligence: Optional[int] = None
    mouthiness: Optional[int] = None
    prey_drive: Optional[float] = None
    barking: Optional[float] = None
    wanderlust: Optional[int] = None
    physical_needs: Optional[float] = None
    energy_level: Optional[int] = None
    intensity: Optional[int] = None
    exercise_needs: Optional[int] = None
    playfulness: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class DogCreate(DogBase):
    pass


class DogOut(DogBase):
    id: int

    model_config = {"from_attributes": True}


class DogListResponse(BaseModel):
    total: int
    items: list[DogOut]
