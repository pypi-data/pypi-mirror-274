from typing import Any

from groq.types.chat.completion_create_params import Message as GroqMessage

from llm_taxi.clients.groq import Groq as GroqClient
from llm_taxi.conversation import Message
from llm_taxi.llms.openai import OpenAI


class Groq(GroqClient, OpenAI):
    def _convert_messages(self, messages: list[Message]) -> list[Any]:
        return [
            GroqMessage(
                role=message.role.value,
                content=message.content,
            )
            for message in messages
        ]
