from llm_taxi.clients.perplexity import Perplexity as PerplexityClient
from llm_taxi.llms.openai import OpenAI


class Perplexity(PerplexityClient, OpenAI):
    pass
