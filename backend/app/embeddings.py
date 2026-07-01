import os

from pydantic_ai import Embedder
from pydantic_ai.embeddings.openai import OpenAIEmbeddingModel
from pydantic_ai.providers.azure import AzureProvider

_EMBEDDING_DEPLOYMENT = os.environ.get(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small"
)

_embedder = Embedder(
    OpenAIEmbeddingModel(
        _EMBEDDING_DEPLOYMENT,
        provider=AzureProvider(
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        ),
    )
)


async def embed_text(text: str) -> list[float]:
    result = await _embedder.embed_documents(text)
    return list(result.embeddings[0])
