from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama, OllamaEmbeddings


def get_client() -> BaseChatModel:
    ollama = ChatOllama(model="qwen2.5:7b")
    return ollama


def get_embeddings_client() -> OllamaEmbeddings:
    ollama = OllamaEmbeddings(model="nomic-embed-text")
    return ollama
