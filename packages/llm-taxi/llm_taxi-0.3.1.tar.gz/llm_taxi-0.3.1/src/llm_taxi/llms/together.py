from llm_taxi.clients.together import Together as TogetherClient
from llm_taxi.llms.openai import OpenAI


class Together(TogetherClient, OpenAI):
    pass
