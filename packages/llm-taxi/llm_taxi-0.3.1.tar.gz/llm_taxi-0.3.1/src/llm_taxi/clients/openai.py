from typing import Any, ClassVar

from llm_taxi.clients.base import Client


class OpenAI(Client):
    env_vars: ClassVar[dict[str, str]] = {
        "api_key": "OPENAI_API_KEY",
    }

    def _init_client(self, **kwargs) -> Any:
        from openai import AsyncClient

        return AsyncClient(**kwargs)
