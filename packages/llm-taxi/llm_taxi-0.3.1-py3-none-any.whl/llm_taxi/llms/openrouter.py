from llm_taxi.clients.openrouter import OpenRouter as OpenRouterClient
from llm_taxi.llms.openai import OpenAI


class OpenRouter(OpenRouterClient, OpenAI):
    pass
