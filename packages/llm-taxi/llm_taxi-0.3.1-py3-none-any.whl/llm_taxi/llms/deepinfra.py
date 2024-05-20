from llm_taxi.clients.deepinfra import DeepInfra as DeepInfraClient
from llm_taxi.llms.openai import OpenAI


class DeepInfra(DeepInfraClient, OpenAI):
    pass
