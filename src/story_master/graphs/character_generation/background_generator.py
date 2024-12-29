from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re


class BackgroundSelector:
    PROMPT = """

    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.output_pattern = re.compile(r"<Output>(.*?)</Output>")
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str):
        pass

    def generate(self):
        pass
