import re
from difflib import get_close_matches

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.entities.character import CharacterType, CHARACTER_TYPE_TABLE
from story_master.log import logger


class CharacterTypeSelector:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Identify the character type based on the description.
    
    -Steps-
    1. Read the character description.
    2. Read the description of the location where the character is.
    3. Read all available character types.
    4. Identify the character type based on the description.
    5. Output the identified character type.
        Output in XML format:
        <CharacterType>Value</CharacterType>
    Don't write any other information.
    The character type should be one of the available character types.
    
    -Character description-
    {character_description}
    
    -Location description-
    {location_description}
    
    -Character types-
    {character_types}
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.output_pattern = re.compile(r"<CharacterType>(.*?)</CharacterType>")
        self.character_types = [
            character_type.value for character_type in CHARACTER_TYPE_TABLE
        ]
        self.character_types_string = " ; ".join(self.character_types)
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> CharacterType:
        try:
            output = output.replace("\n", " ").strip()
            match = self.output_pattern.search(output)
            raw_character_type = match.group(1).strip()
            character_type = get_close_matches(
                raw_character_type, self.character_types
            )[0]
            return CharacterType(character_type)
        except Exception:
            logger.error(f"CharacterTypeSelector. Failed to parse output: {output}")
            return CharacterType.COMMONER

    def generate(
        self, character_description: str, location_description: str
    ) -> CharacterType:
        character_type = self.chain.invoke(
            {
                "character_description": character_description,
                "location_description": location_description,
                "character_types": self.character_types_string,
            }
        )
        return character_type
