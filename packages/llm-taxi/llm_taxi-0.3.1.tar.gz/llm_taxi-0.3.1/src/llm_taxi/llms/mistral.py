from collections.abc import AsyncGenerator
from typing import Any

from mistralai.models.chat_completion import ChatMessage

from llm_taxi.clients.mistral import Mistral as MistralClient
from llm_taxi.conversation import Message
from llm_taxi.llms.base import LLM
from llm_taxi.llms.openai import streaming_response


class Mistral(MistralClient, LLM):
    def _convert_messages(self, messages: list[Message]) -> list[Any]:
        return [ChatMessage(role=x.role.value, content=x.content) for x in messages]

    async def streaming_response(
        self,
        messages: list[Message],
        **kwargs,
    ) -> AsyncGenerator:
        messages = self._convert_messages(messages)

        response = self.client.chat_stream(
            messages=messages,
            **self._get_call_kwargs(**kwargs),
        )

        return streaming_response(response)

    async def response(self, messages: list[Message], **kwargs) -> str:
        messages = self._convert_messages(messages)

        response = await self.client.chat(
            messages=messages,
            **self._get_call_kwargs(**kwargs),
        )

        return response.choices[0].message.content
