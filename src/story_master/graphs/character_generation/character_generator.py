from langchain_core.language_models.chat_models import BaseChatModel
from story_master.graphs.character_generation.race_generator import RaceGenerator
from story_master.graphs.character_generation.class_generator import ClassGenerator
from story_master.graphs.character_generation.background_generator import (
    BackgroundGenerator,
)
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
from difflib import get_close_matches
from story_master.entities.character import Gender, GENDERS, Character
from story_master.entities.alignment import AlignmentType, ALIGNMENTS


class CharacterParameterGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Generate parameters for the character described.

    -Steps-
    1. Read the character description.
    2. Generate character gender.
        Pick any value from {genders}
        Output in XML format:
        <Gender>Value</Gender>
    3. Generate character age.
        Pick any suitable number.
        Output in XML format:
        <Age>Value</Age>
    4. Generate character alignment.
        Pick any value from {alignments}
        Output in XML format:
        <Alignment>Value</Alignment>
    5. Output the generated parameters in XML format, one per line.
        Example output:
        <Gender>Female</Gender>
        <Age>25</Age>
        <Alignment>Good</Alignment>        

    -Character description-
    {character_description}
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.gender_pattern = re.compile(r"<Gender>(.*)</Gender>")
        self.age_pattern = re.compile(r"<Age>(.*)</Age>")
        self.alignment_pattern = re.compile(r"<Alignment>(.*)</Alignment>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str):
        print("Raw output")
        print(output)
        raw_gender_match = self.gender_pattern.search(output)
        raw_age_match = self.age_pattern.search(output)
        raw_alignment_match = self.alignment_pattern.search(output)
        gender = get_close_matches(
            raw_gender_match.group(1).lower(), [item.value for item in GENDERS]
        )[0]
        age = int(raw_age_match.group(1))
        alignment = get_close_matches(
            raw_alignment_match.group(1).lower().capitalize(),
            [item.value for item in ALIGNMENTS],
        )[0]
        gender = Gender(gender)
        alignment = AlignmentType(alignment)
        return gender, age, alignment

    def create_genders_description(self) -> str:
        return "; ".join([item.name for item in GENDERS])

    def create_alignments_description(self) -> str:
        return "; ".join([item.name for item in ALIGNMENTS])

    def generate(self, character_description: str):
        gender_description = self.create_genders_description()
        alignment_description = self.create_alignments_description
        gender, age, alignment = self.chain.invoke(
            {
                "genders": gender_description,
                "alignments": alignment_description,
                "character_description": character_description,
            }
        )
        return gender, age, alignment


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
        match = self.output_pattern.search(output)
        return match.group(1)

    def generate(self, character_description: str, available_names: list[str]) -> str:
        names = "; ".join(available_names)
        name = self.chain.invoke(
            {"available_names": names, "character_description": character_description}
        )
        return name


class CharacterGenerator:
    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.race_generator = RaceGenerator(self.llm_model)
        self.class_generator = ClassGenerator(self.llm_model)
        self.background_generator = BackgroundGenerator(self.llm_model)
        self.character_parameter_generator = CharacterParameterGenerator(self.llm_model)
        self.character_name_generator = CharacterNameGenerator(self.llm_model)

    def generate(self, character_description: str) -> Character:
        race = self.race_generator.generate(character_description)
        character_description += f"\n Race: {race.get_full_description()} \n"
        class_object = self.class_generator.generate(character_description)
        character_description += (
            f"\n Class: {class_object.get_short_class_description()} \n"
        )
        background = self.background_generator.generate(character_description)
        character_description += f"\n Background: {background.description} \n"

        gender, age, alignment = self.character_parameter_generator.generate(
            character_description
        )
        print("Picked parameters")
        print(gender, age, alignment)

        name = self.character_name_generator.generate(character_description, race.names)
        print("Picked name")
        print(name)
        strength = class_object.base_strength + race.strength_bonus
        agility = class_object.base_agility + race.agility_bonus
        constitution = class_object.base_constitution + race.constitution_bonus
        intelligence = class_object.base_intelligence + race.intelligence_bonus
        wisdom = class_object.base_wisdom + race.wisdom_bonus
        charisma = class_object.base_charisma + race.charisma_bonus

        character = Character(
            name=name,
            sex=gender,
            age=age,
            alignment=alignment,
            strength=strength,
            agility=agility,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            race=race,
            klass=class_object,
            background=background,
            traits=background.selected_trait,
            ideal=background.selected_ideal[0],
            bond=background.selected_bond[0],
            flaw=background.selected_flaw[0],
        )

        return character
