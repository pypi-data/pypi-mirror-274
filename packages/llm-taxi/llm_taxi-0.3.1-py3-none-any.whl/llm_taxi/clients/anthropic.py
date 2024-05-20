from typing import Any, ClassVar

from anthropic import AsyncAnthropic

from llm_taxi.clients.base import Client


class Anthropic(Client):
    env_vars: ClassVar[dict[str, str]] = {
        "api_key": "ANTHROPIC_API_KEY",
    }

    def _init_client(self, **kwargs) -> Any:
        return AsyncAnthropic(**kwargs)
