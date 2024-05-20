import abc


class Embedding(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError

    @abc.abstractmethod
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError
