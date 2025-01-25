import random
import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger


class CharacterNameGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Generate a name for the character described.

    -Steps-
    1. Read the character description.
    2. Read examples of available names.
    3. Generate a name that fits this character. 
        You should pay attention to the character's race and background.
    4. Output the generated name in XML format.
        Example output: <Output>Value</Output>

    -Available names-
    {available_names}

    -Character description-
    {character_description}

    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.output_pattern = re.compile(r"<Output>(.*)</Output>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> str:
        try:
            match = self.output_pattern.search(output)
            return match.group(1)
        except Exception as e:
            logger.error(f"CharacterNameGenerator. Failed to parse output: {output}")
            raise e

    def generate(
        self,
        character_description: str,
        available_names: list[str],
        existing_names: set[str],
    ) -> str:
        for existing_name in existing_names:
            pair = existing_name.split()
            available_names = [
                name
                for name in available_names
                if pair[0] not in name and pair[-1] not in name
            ]

        available_names_string = "; ".join(available_names)
        try:
            name = self.chain.invoke(
                {
                    "available_names": available_names_string,
                    "character_description": character_description,
                }
            )
            return name
        except Exception:
            return random.choice(available_names)
