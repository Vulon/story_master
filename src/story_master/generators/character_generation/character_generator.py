import re
from difflib import get_close_matches

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel

from story_master.entities.character import (
    GENDERS,
    Character,
    Gender,
    Settler,
)


from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.log import logger


class BaseCharacterInfo(BaseModel):
    gender: Gender
    age: int
    name: str
    character_description: str
    appearance: str


class CharacterParameterGenerator:
    PROMPT = """
    You are a character generation agent for a simulation game.

    -Goal-
    Generate parameters for the character described.

    -Steps-
    1. Read the character description.
    2. Generate character gender.
        Pick any value from {genders}
    3. Generate character age.
        Pick any suitable integer number.
    4. Generate character name.
        Use the character description to generate a name.
    5. Generate a character appearance. 
        Write how the character looks like.
        You can be creative and add any details you want.        
    6. Output the generated parameters in XML format, one per line.

    -Character description-
    {character_description}
    
    -Output format-
    <Gender>Gender</Gender>
    <Age>Age</Age>
    <Name>Name</Name>
    <Appearance>Appearance</Appearance>
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.gender_pattern = re.compile(r"<Gender>(.*?)</Gender>")
        self.age_pattern = re.compile(r"<Age>(.*?)</Age>")
        self.name_pattern = re.compile(r"<Name>(.*?)</Name>")
        self.apperance_pattern = re.compile(r"<Appearance>(.*?)</Appearance>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str):
        output = output.replace("\n", " ")
        try:
            raw_gender_match = self.gender_pattern.search(output)
            gender = get_close_matches(
                raw_gender_match.group(1).lower(), [item.value for item in GENDERS]
            )[0]
            gender = Gender(gender)

            raw_age_match = self.age_pattern.search(output)
            age = int(raw_age_match.group(1))

            raw_name_match = self.name_pattern.search(output)
            name = raw_name_match.group(1)

            raw_appearance_match = self.apperance_pattern.search(output)
            appearance = raw_appearance_match.group(1)
            return gender, age, name, appearance

        except Exception as e:
            logger.error(
                f"CharacterParameterGenerator. Could not parse output: {output}"
            )
            raise e

    def create_genders_description(self) -> str:
        return "; ".join([item.name for item in GENDERS])

    def generate(self, character_description: str):
        gender_description = self.create_genders_description()
        return self.chain.invoke(
            {
                "genders": gender_description,
                "character_description": character_description,
            }
        )


class CharacterGenerator:
    def __init__(
        self,
        llm_model: BaseChatModel,
        storage_handler: StorageHandler,
        summary_handler: SummaryHandler,
    ):
        self.llm_model = llm_model
        self.summary_handler = summary_handler
        self.storage_handler = storage_handler
        self.character_parameter_generator = CharacterParameterGenerator(self.llm_model)

    def _create_base_character_info(
        self, character_description: str
    ) -> BaseCharacterInfo:
        gender, age, name, appearance = self.character_parameter_generator.generate(
            character_description
        )
        character_description += f" Sex: {gender}, Age: {age}. Name: {name} "

        existing_names = self.storage_handler.get_existing_names()

        return BaseCharacterInfo(
            gender=gender,
            age=age,
            name=name,
            character_description=character_description,
            appearance=appearance,
        )

    def generate(self, character_description: str) -> Character:
        base_character_info = self._create_base_character_info(character_description)

        character = Settler(
            name=base_character_info.name,
            age=base_character_info.age,
            gender=base_character_info.gender,
            appearance=base_character_info.appearance,
        )

        return character
