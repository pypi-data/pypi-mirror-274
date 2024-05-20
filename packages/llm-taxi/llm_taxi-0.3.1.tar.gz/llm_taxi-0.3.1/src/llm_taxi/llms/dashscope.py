from llm_taxi.clients.dashscope import DashScope as DashScopeClient
from llm_taxi.llms.openai import OpenAI


class DashScope(DashScopeClient, OpenAI):
    pass
