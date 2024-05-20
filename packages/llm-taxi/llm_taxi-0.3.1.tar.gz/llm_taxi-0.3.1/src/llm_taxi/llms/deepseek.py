from llm_taxi.clients.deepseek import DeepSeek as DeepSeekClient
from llm_taxi.llms.openai import OpenAI


class DeepSeek(DeepSeekClient, OpenAI):
    pass
