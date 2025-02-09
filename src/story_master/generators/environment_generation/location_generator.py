import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger

from story_master.storage.map.map_model import BaseLocation


class LocationGenerator:
    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model

