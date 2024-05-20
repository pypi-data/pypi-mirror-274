from typing import Any, ClassVar

from groq import AsyncGroq

from llm_taxi.clients.openai import OpenAI


class Groq(OpenAI):
    env_vars: ClassVar[dict[str, str]] = {
        "api_key": "GROQ_API_KEY",
    }

    def _init_client(self, **kwargs) -> Any:
        return AsyncGroq(**kwargs)
