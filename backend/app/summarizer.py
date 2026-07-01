import logging
import os
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_ai.settings import ModelSettings

logger = logging.getLogger("app.summarizer")

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(name: str) -> str:
    return (_PROMPTS_DIR / name).read_text(encoding="utf-8").strip()


@dataclass
class BreedFacts:
    breed_name: str
    size: str | None = None
    breed_group: str | None = None
    height: str | None = None
    weight: str | None = None
    life_span: str | None = None
    adaptability: float | None = None
    apartment_friendly: int | None = None
    good_for_novice: int | None = None
    sensitivity: int | None = None
    tolerates_alone: int | None = None
    tolerates_cold: int | None = None
    tolerates_hot: int | None = None
    friendliness: float | None = None
    affectionate_family: int | None = None
    kid_friendly: int | None = None
    dog_friendly: int | None = None
    stranger_friendly: int | None = None
    shedding: int | None = None
    drooling: float | None = None
    easy_groom: int | None = None
    general_health: int | None = None
    trainability: float | None = None
    easy_train: int | None = None
    intelligence: int | None = None
    mouthiness: int | None = None
    prey_drive: float | None = None
    barking: float | None = None
    wanderlust: int | None = None
    energy_level: int | None = None
    intensity: int | None = None
    exercise_needs: int | None = None
    playfulness: int | None = None
    description: str | None = None


class BreedSummary(BaseModel):
    summary: str = Field(
        description=(
            "One paragraph, 4-6 sentences, 90-130 words, first-person from the "
            "perspective of a prospective owner describing the kind of dog they want. "
            "Never names the breed and never restates column names or numeric scores."
        )
    )


_summarizer_model = OpenAIChatModel(
    os.environ.get("AZURE_OPENAI_SUMMARIZER_MODEL", "gpt-5.4-mini"),
    provider=AzureProvider(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    ),
)

summarizer_agent = Agent(
    _summarizer_model,
    output_type=BreedSummary,
    deps_type=BreedFacts,
    system_prompt=_load_prompt("breed_summary_prompt.md"),
    model_settings=ModelSettings(temperature=0.1),
)


@summarizer_agent.instructions
def inject_breed_facts(ctx: RunContext[BreedFacts]) -> str:
    d = ctx.deps

    def score(val: int | float | None) -> str:
        if val is None:
            return "unknown"
        return f"{val}/5"

    return (
        "Facts about this breed (do NOT name the breed or restate these labels "
        "in your output):\n"
        f"Size: {d.size or 'unknown'}\n"
        f"Breed group: {d.breed_group or 'unknown'}\n"
        f"Height: {d.height or 'unknown'}\n"
        f"Weight: {d.weight or 'unknown'}\n"
        f"Life span: {d.life_span or 'unknown'}\n"
        f"Description: {d.description or 'N/A'}\n\n"
        "Scores (1-5 scale, higher = more of that trait):\n"
        f"  Adaptability: {score(d.adaptability)}\n"
        f"  Apartment friendly: {score(d.apartment_friendly)}\n"
        f"  Good for novice owners: {score(d.good_for_novice)}\n"
        f"  Sensitivity: {score(d.sensitivity)}\n"
        f"  Tolerates being alone: {score(d.tolerates_alone)}\n"
        f"  Tolerates cold weather: {score(d.tolerates_cold)}\n"
        f"  Tolerates hot weather: {score(d.tolerates_hot)}\n"
        f"  Friendliness: {score(d.friendliness)}\n"
        f"  Affectionate with family: {score(d.affectionate_family)}\n"
        f"  Kid friendly: {score(d.kid_friendly)}\n"
        f"  Dog friendly: {score(d.dog_friendly)}\n"
        f"  Stranger friendly: {score(d.stranger_friendly)}\n"
        f"  Shedding: {score(d.shedding)}\n"
        f"  Drooling: {score(d.drooling)}\n"
        f"  Easy to groom: {score(d.easy_groom)}\n"
        f"  General health: {score(d.general_health)}\n"
        f"  Trainability: {score(d.trainability)}\n"
        f"  Easy to train: {score(d.easy_train)}\n"
        f"  Intelligence: {score(d.intelligence)}\n"
        f"  Mouthiness: {score(d.mouthiness)}\n"
        f"  Prey drive: {score(d.prey_drive)}\n"
        f"  Barking tendency: {score(d.barking)}\n"
        f"  Wanderlust: {score(d.wanderlust)}\n"
        f"  Energy level: {score(d.energy_level)}\n"
        f"  Intensity: {score(d.intensity)}\n"
        f"  Exercise needs: {score(d.exercise_needs)}\n"
        f"  Playfulness: {score(d.playfulness)}\n"
    )


async def summarize_breed(facts: BreedFacts) -> str:
    result = await summarizer_agent.run(
        "Write the owner-perspective paragraph.", deps=facts
    )
    return result.output.summary
