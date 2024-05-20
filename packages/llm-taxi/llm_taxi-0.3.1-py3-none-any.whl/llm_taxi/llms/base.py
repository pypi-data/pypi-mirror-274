import abc
from collections.abc import AsyncGenerator
from typing import Any

from llm_taxi.conversation import Message


class LLM(metaclass=abc.ABCMeta):
    def _convert_messages(self, messages: list[Message]) -> list[Any]:
        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]

    @abc.abstractmethod
    async def streaming_response(
        self,
        messages: list[Message],
        **kwargs,
    ) -> AsyncGenerator:
        raise NotImplementedError

    @abc.abstractmethod
    async def response(self, messages: list[Message], **kwargs) -> str:
        raise NotImplementedError
