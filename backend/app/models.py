import os

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, Float, Text

from app.database import Base

EMBEDDING_DIM = int(os.environ.get("AZURE_OPENAI_EMBEDDING_DIMENSIONS", "1536"))


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    breed_name = Column(String(255), unique=True, nullable=False, index=True)
    size = Column(String(50))
    breed_group = Column(String(100))
    height = Column(String(100))
    avg_height_cm = Column(Float)
    weight = Column(String(100))
    avg_weight_kg = Column(Float)
    life_span = Column(String(100))
    avg_life_span_years = Column(Float)
    adaptability = Column(Float)
    apartment_friendly = Column(Integer)
    good_for_novice = Column(Integer)
    sensitivity = Column(Integer)
    tolerates_alone = Column(Integer)
    tolerates_cold = Column(Integer)
    tolerates_hot = Column(Integer)
    friendliness = Column(Float)
    affectionate_family = Column(Integer)
    kid_friendly = Column(Integer)
    dog_friendly = Column(Integer)
    stranger_friendly = Column(Integer)
    health_grooming = Column(Float)
    shedding = Column(Integer)
    drooling = Column(Float)
    easy_groom = Column(Integer)
    general_health = Column(Integer)
    weight_gain_potential = Column(Integer)
    size_score = Column(Integer)
    trainability = Column(Float)
    easy_train = Column(Integer)
    intelligence = Column(Integer)
    mouthiness = Column(Integer)
    prey_drive = Column(Float)
    barking = Column(Float)
    wanderlust = Column(Integer)
    physical_needs = Column(Float)
    energy_level = Column(Integer)
    intensity = Column(Integer)
    exercise_needs = Column(Integer)
    playfulness = Column(Integer)
    description = Column(Text)
    image_url = Column(String(500))
    owner_summary = Column(Text)
    embedding = Column(Vector(EMBEDDING_DIM))
