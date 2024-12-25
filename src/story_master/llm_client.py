from langchain_ollama import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel


def get_client() -> BaseChatModel:
    ollama = ChatOllama(model="qwen2.5:7b")
    return ollama
