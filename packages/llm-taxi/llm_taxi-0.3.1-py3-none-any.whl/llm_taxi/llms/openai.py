from collections.abc import AsyncGenerator
from typing import Any

from llm_taxi.clients.openai import OpenAI as OpenAIClient
from llm_taxi.conversation import Message
from llm_taxi.llms.base import LLM


async def streaming_response(response: Any) -> AsyncGenerator:
    async for chunk in response:
        if content := chunk.choices[0].delta.content:
            yield content


class OpenAI(OpenAIClient, LLM):
    async def streaming_response(
        self,
        messages: list[Message],
        **kwargs,
    ) -> AsyncGenerator:
        messages = self._convert_messages(messages)

        response = await self.client.chat.completions.create(
            messages=messages,
            stream=True,
            **self._get_call_kwargs(**kwargs),
        )

        return streaming_response(response)

    async def response(self, messages: list[Message], **kwargs) -> str:
        messages = self._convert_messages(messages)

        response = await self.client.chat.completions.create(
            messages=messages,
            **self._get_call_kwargs(**kwargs),
        )

        if content := response.choices[0].message.content:
            return content

        return ""
