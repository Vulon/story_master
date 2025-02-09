import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.entities.character import Character
from story_master.storage.map.map_model import BaseLocation
from story_master.storage.memory.memory_model import Observation
from story_master.storage.storage_manager import StorageManager
from story_master.log import logger


class SummaryAgent:
    PROMPT = """
    You are a Dungeons and Dragons summary agent.

    -Goal-
    Summarize the provided information.
    
    -Steps-
    1. Read the context explaining what information is needed.
    2. Read provided information.
    3. Summarize the information.
        Include all important details that are relevant to the context.
    4. Output the summary in XML format.
        Format: <Summary>Summary</Summary>
        Don't output anything else apart from the summary.
        
    -Context-
    {context}
    
    -Information-
    {information}
    
    ########
    Output:
    """

    def __init__(self, storage_manager: StorageManager, llm_model: BaseChatModel):
        self.storage_manager = storage_manager
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.pattern = re.compile(r"<Summary>(.*?)</Summary>")
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str):
        try:
            output = output.replace("\n", " ")
            match = self.pattern.search(output)
            return match.group(1)
        except Exception:
            logger.error(f"SummaryAgent. Could not parse: {output}")
            return None

    def get_summary(self, context: str, information: str):
        summary = self.chain.invoke(
            {
                "context": context,
                "information": information,
            }
        )
        if summary:
            return summary
        return information

    def summarize_location(self, context: str, location: BaseLocation) -> str:
        information = location.get_description()
        return self.get_summary(context, information)

    def summarize_character(self, context: str, character: Character) -> str:
        information = character.get_description()
        return self.get_summary(context, information)

    def format_memories(self, memories: list[Observation]) -> str:
        strings = []
        for memory in memories:
            strings.append(f"{memory.title}: {memory.content}")
        memories_string = " \n ".join(strings)
        return f"<Memory>{memories_string}</Memory>"

    def summarize_memories(self, context: str, memories: list[Observation]) -> str:
        information = self.format_memories(memories)
        return self.get_summary(context, information)
