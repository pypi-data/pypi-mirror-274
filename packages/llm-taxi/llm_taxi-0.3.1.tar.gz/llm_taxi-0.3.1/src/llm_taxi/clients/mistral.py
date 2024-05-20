from typing import Any, ClassVar

from mistralai.async_client import MistralAsyncClient

from llm_taxi.clients.openai import OpenAI


class Mistral(OpenAI):
    env_vars: ClassVar[dict[str, str]] = {
        "api_key": "MISTRAL_API_KEY",
    }

    def _init_client(self, **kwargs) -> Any:
        kwargs.pop("base_url", None)

        return MistralAsyncClient(**kwargs)
