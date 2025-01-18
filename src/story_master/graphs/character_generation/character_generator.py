import re
from difflib import get_close_matches

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.entities.alignment import ALIGNMENTS, AlignmentType
from story_master.entities.character import (
    GENDERS,
    Character,
    CharacterType,
    Adventurer,
    Merchant,
    Commoner,
    Gender,
    calculate_bonus_from_characteristics,
)
import random
from story_master.entities.items.items import Item, ItemStack
from story_master.graphs.character_generation.background_generator import (
    BackgroundGenerator,
)
from story_master.graphs.character_generation.class_generator import (
    AdventurerClassGenerator,
)
from story_master.graphs.character_generation.race_generator import RaceGenerator
from story_master.graphs.character_generation.name_generator import (
    CharacterNameGenerator,
)
from story_master.graphs.character_generation.character_type_selector import (
    CharacterTypeSelector,
)
from story_master.entities.classes import (
    CivilianClass,
)
from story_master.storage.map.map_model import Location
from story_master.graphs.character_generation.items_generator import (
    MerchantStockGenerator,
)


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


def remove_duplicates(items: list[Item]) -> list[Item]:
    names = set()
    unique_items = []
    for item in items:
        if item.name not in names:
            unique_items.append(item)
            names.add(item.name)
    return unique_items


class CharacterGenerator:
    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.race_generator = RaceGenerator(self.llm_model)
        self.class_generator = AdventurerClassGenerator(self.llm_model)
        self.background_generator = BackgroundGenerator(self.llm_model)
        self.character_parameter_generator = CharacterParameterGenerator(self.llm_model)
        self.character_name_generator = CharacterNameGenerator(self.llm_model)
        self.character_type_selector = CharacterTypeSelector(self.llm_model)
        self.merchant_stock_generator = MerchantStockGenerator(self.llm_model)

    def _get_item_stacks(self, raw_items: list[Item]) -> dict[str, ItemStack]:
        items_map = {item.name: item for item in raw_items}
        item_quantities = {name: 0 for name in items_map.keys()}
        for item in raw_items:
            item_quantities[item.name] += item.base_quantity
        item_stacks = {
            name:
            ItemStack(item=items_map[name], quantity=quantity)
            for name, quantity in item_quantities.items()
        }
        return item_stacks

    def _create_adventurer(self, character_description: str) -> Adventurer:
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

        level = 1

        saving_throws = class_object.saving_throws

        armor_proficiencies = remove_duplicates(
            class_object.armor_proficiencies + race.armor_proficiencies
        )
        weapon_proficiencies = sorted(
            set(class_object.weapon_proficiencies + race.weapon_proficiencies)
        )
        skills = sorted(set(class_object.skills + race.skills + background.skills))
        raw_items = class_object.starting_items + background.equipment
        item_stacks = self._get_item_stacks(raw_items)

        tool_proficiencies = (
            background.tool_proficiencies + race.instrument_proficiencies
        )
        tool_proficiencies = remove_duplicates(tool_proficiencies)
        money = class_object.starting_money + background.money
        perks = remove_duplicates(class_object.get_perks(level) + race.perks)

        max_health = class_object.health_dice + calculate_bonus_from_characteristics(
            constitution
        )

        # TODO: Implement level up mechanic

        character = Adventurer(
            type=CharacterType.ADVENTURER,
            name=name,
            sex=gender,
            age=age,
            alignment=alignment,
            max_health=max_health,
            current_health=max_health,
            strength=strength,
            agility=agility,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            race=race,
            klass=class_object,
            background=background,
            level=level,
            saving_throws=saving_throws,
            armor_proficiencies=armor_proficiencies,
            weapon_proficiencies=weapon_proficiencies,
            skills=skills,
            items=item_stacks,
            tool_proficiencies=tool_proficiencies,
            perks=perks,
            money=money,
        )

        return character

    def _create_commoner(self, character_description: str) -> Commoner:
        # TODO: dynamically generate items and tool proficiencies
        race = self.race_generator.generate(character_description)
        character_description += f"\n Race: {race.get_full_description()} \n"

        class_object = CivilianClass()
        character_description += (
            f"\n Class: {class_object.get_short_class_description()} \n"
        )

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

        level = 1

        raw_items = class_object.starting_items
        item_stacks = self._get_item_stacks(raw_items)
        tool_proficiencies = race.instrument_proficiencies
        tool_proficiencies = remove_duplicates(tool_proficiencies)
        money = 10 + random.randint(0, 10)

        max_health = class_object.health_dice + calculate_bonus_from_characteristics(
            constitution
        )

        # TODO: Implement level up mechanic

        character = Commoner(
            type=CharacterType.COMMONER,
            name=name,
            sex=gender,
            age=age,
            alignment=alignment,
            max_health=max_health,
            current_health=max_health,
            strength=strength,
            agility=agility,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            race=race,
            level=level,
            items=item_stacks,
            tool_proficiencies=tool_proficiencies,
            money=money,
            klass=class_object,
        )

        return character

    def _create_merchant(
        self, character_description: str, location: Location
    ) -> Merchant:
        # TODO: dynamically generate items
        race = self.race_generator.generate(character_description)
        character_description += f"\n Race: {race.get_full_description()} \n"

        class_object = CivilianClass()
        character_description += (
            f"\n Class: {class_object.get_short_class_description()} \n"
        )

        gender, age, alignment = self.character_parameter_generator.generate(
            character_description
        )
        print("Picked parameters")
        print(gender, age, alignment)

        name = self.character_name_generator.generate(character_description, race.names)
        print("Picked name")
        print(name)
        raw_stock_items = self.merchant_stock_generator.generate(
            character_description, location
        )
        stock_stacks = self._get_item_stacks(raw_stock_items)

        strength = class_object.base_strength + race.strength_bonus
        agility = class_object.base_agility + race.agility_bonus
        constitution = class_object.base_constitution + race.constitution_bonus
        intelligence = class_object.base_intelligence + race.intelligence_bonus
        wisdom = class_object.base_wisdom + race.wisdom_bonus
        charisma = class_object.base_charisma + race.charisma_bonus

        level = 1

        raw_items = class_object.starting_items
        item_stacks = self._get_item_stacks(raw_items)

        money = 20 + random.randint(-5, 30)

        max_health = class_object.health_dice + calculate_bonus_from_characteristics(
            constitution
        )

        # TODO: Implement level up mechanic

        character = Merchant(
            type=CharacterType.MERCHANT,
            name=name,
            sex=gender,
            age=age,
            alignment=alignment,
            max_health=max_health,
            current_health=max_health,
            strength=strength,
            agility=agility,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            race=race,
            level=level,
            items=item_stacks,
            money=money,
            klass=class_object,
            stock=stock_stacks,
        )

        return character

    def generate(
        self, character_description: str, is_player: bool, location: Location
    ) -> Character:
        if is_player:
            character_type = CharacterType.ADVENTURER
        else:
            character_type = self.character_type_selector.generate(
                character_description, location
            )
        print("Picked character type", str(character_type))
        if character_type == CharacterType.ADVENTURER:
            return self._create_adventurer(character_description)
        elif character_type == CharacterType.COMMONER:
            return self._create_commoner(character_description)
        elif character_type == CharacterType.MERCHANT:
            return self._create_merchant(character_description, location)
        else:
            raise ValueError(f"Unsupported character type: {character_type}")
