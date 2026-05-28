import asyncio
import logging
import os
import uuid
from dataclasses import dataclass
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider

logger = logging.getLogger("app.agent")

_sessions: dict[str, list[ModelMessage]] = {}

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(name: str) -> str:
    return (_PROMPTS_DIR / name).read_text(encoding="utf-8").strip()


@dataclass
class DogContext:
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
    easy_groom: int | None = None
    general_health: int | None = None
    trainability: float | None = None
    easy_train: int | None = None
    intelligence: int | None = None
    barking: float | None = None
    energy_level: int | None = None
    exercise_needs: int | None = None
    playfulness: int | None = None
    description: str | None = None


class ChatResult(BaseModel):
    answer: str = Field(description="The answer to the user's question about the dog breed")


model = OpenAIChatModel(
    "gpt-4.1-mini",
    provider=AzureProvider(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    ),
)

chat_agent = Agent(
    model,
    output_type=ChatResult,
    deps_type=DogContext,
    system_prompt=_load_prompt("system_prompt.md"),
)


@chat_agent.instructions
def inject_dog_context(ctx: RunContext[DogContext]) -> str:
    d = ctx.deps

    def score(val: int | float | None) -> str:
        if val is None:
            return "unknown"
        return f"{val}/5"

    return (
        f"Breed: {d.breed_name}\n"
        f"Size: {d.size or 'unknown'}\n"
        f"Breed group: {d.breed_group or 'unknown'}\n"
        f"Height: {d.height or 'unknown'}\n"
        f"Weight: {d.weight or 'unknown'}\n"
        f"Life span: {d.life_span or 'unknown'}\n"
        f"Description: {d.description or 'N/A'}\n\n"
        f"Scores (1–5 scale):\n"
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
        f"  Easy to groom: {score(d.easy_groom)}\n"
        f"  General health: {score(d.general_health)}\n"
        f"  Trainability: {score(d.trainability)}\n"
        f"  Easy to train: {score(d.easy_train)}\n"
        f"  Intelligence: {score(d.intelligence)}\n"
        f"  Barking tendency: {score(d.barking)}\n"
        f"  Energy level: {score(d.energy_level)}\n"
        f"  Exercise needs: {score(d.exercise_needs)}\n"
        f"  Playfulness: {score(d.playfulness)}\n"
    )


async def answer_dog_question(
    context: DogContext, question: str, session_id: str | None = None
) -> tuple[str, str]:
    if session_id is None:
        session_id = str(uuid.uuid4())
    history = _sessions.get(session_id, [])
    try:
        result = await asyncio.wait_for(
            chat_agent.run(question, deps=context, message_history=history),
            timeout=15.0,
        )
        _sessions[session_id] = result.all_messages()
        return result.output.answer, session_id
    except asyncio.TimeoutError:
        logger.warning("Chat timed out for breed: %s", context.breed_name)
        raise HTTPException(status_code=504, detail="Request timed out")
    except Exception:
        logger.exception("Unexpected error in chat for breed: %s", context.breed_name)
        raise HTTPException(status_code=502, detail="Failed to get a response from the AI")
