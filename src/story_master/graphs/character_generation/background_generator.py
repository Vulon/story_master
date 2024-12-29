from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
import random
from difflib import get_close_matches
from story_master.entities.background import BackgroundType, BACKGROUNDS, Background
from story_master.utils.selection import SomeOf


class BackgroundChoiceSelector:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Generate a background detail for the character described.

    -Steps-
    1. Read the character description.
    2. Read what you need to choose.
    3. Read all options that you can choose from.
    4. Read how many options you need to choose.
    5. Generate background details.
       A detail is usually a single sentence. 
       It can be a Trait, Ideal, Bond, Flaw, or other background detail.
       You need to generate as many details as the -Count- specifies.
       For every detail, you need to choose one option from the -Choices- list.
    6. Output the generated background details in XML format.
        Every detail should be enclosed in <Output> tags.
        Don't add any other tags.
        Example output: 
        <Output>Background detail</Output>
        <Output>Background detail 2</Output>

    -Character description-
    {character_description}

    -Choice description-
    {choice_description}

    -Choices-
    {choices}

    -Count-
    {count}

    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.output_pattern = re.compile(r"<Output>(.*?)</Output>")
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser()

    def parse_output(self, output: str) -> list[str]:
        details = self.output_pattern.findall(output)
        return details

    def generate(
        self,
        character_description: str,
        choice_description: str,
        choices: list[str],
        count: int,
    ) -> list[str]:
        raw_output = self.chain.invoke(
            {
                "character_description": character_description,
                "choice_description": choice_description,
                "choices": choices,
                "count": count,
            }
        )
        try:
            return self.parse_output(raw_output)
        except Exception:
            print("Could not parse output:", raw_output)
            return random.choice(choices)


class BackgroundSelector:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Select a background for the character described.

    -Steps-
    1. Read the character description.
    2. Read all available backgrounds.
    3. Select the background that best fits the character's description.
    4. Output the name of the selected background in XML format.
       Example output: <Output>BackgroundName</Output>       

    -Available backgrounds-
    {backgrounds}

    -Character description-
    {character_description}

    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.output_pattern = re.compile(r"<Output>(.*?)</Output>")
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def create_all_background_descriptions(self) -> str:
        descriptions = []
        for background_type, background in BACKGROUNDS.items():
            descriptions.append(
                f"(Name: {background_type.value} | description: {background.description})"
            )
        return "\n".join(descriptions)

    def parse_output(self, output: str) -> BackgroundType:
        match = self.output_pattern.search(output)
        parsed_string = get_close_matches(
            match.group(1), [item.value for item in BACKGROUNDS.keys()]
        )[0]
        return BackgroundType(parsed_string)

    def generate(self, character_description: str):
        backgrounds_description = self.create_all_background_descriptions()
        background_type = self.chain.invoke(
            {
                "backgrounds": backgrounds_description,
                "character_description": character_description,
            }
        )
        return background_type


class ItemSelector:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Select items that the character described should have.

    -Steps-
    1. Read the character description.
    2. Read what items you can pick. 
    3. Read how many items you need to pick.
    4. Read the task details.
    5. Pick items that best fit the character's description according to the task details.
    6. Output the names of the selected items in XML format.
         Example output: <Output>ItemName</Output><Output>ItemName2</Output>
    
    -Character description-
    {character_description}

    -Items-
    {items}

    -Count-
    {count}

    -Task description-
    {task_description}

    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.output_pattern = re.compile(r"<Output>(.*?)</Output>")
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser()

    def parse_output(self, output: str, clean_values: list[str]) -> list[str]:
        raw_items = self.output_pattern.findall(output)
        items = []
        for raw_item in raw_items:
            item = get_close_matches(raw_item, clean_values)[0]
            items.append(item)
        return items

    def split_some_of(self, values: list) -> tuple[list[SomeOf], list]:
        some_of_values = []
        single_values = []
        for item in values:
            if isinstance(item, SomeOf):
                some_of_values.append(item)
            else:
                single_values.append(item)
        return some_of_values, single_values

    def pick_items(
        self, character_description: str, some_of: SomeOf, task_description: str
    ) -> list:
        choices = [item.name for item in some_of.items]
        raw_output = self.chain.invoke(
            {
                "character_description": character_description,
                "items": choices,
                "count": some_of.count,
                "task_description": task_description,
            }
        )
        item_names = self.parse_output(raw_output, choices)
        print("Picked", item_names)
        return [item for item in some_of.items if item.name in item_names]

    def generate(
        self,
        character_description: str,
        input_items: SomeOf | list,
        task_description: str,
    ) -> list[str]:
        if isinstance(input_items, SomeOf):
            picked_items = self.pick_items(
                character_description, input_items, task_description
            )
            return picked_items

        elif isinstance(input_items, list):
            some_of_values, single_values = self.split_some_of(input_items)
            for item in some_of_values:
                picked_items = self.pick_items(
                    character_description, item, task_description
                )
                single_values += picked_items
            return single_values

        return input_items


# TODO: We need to pick items from SomeOf


class BackgroundGenerator:
    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.background_selector = BackgroundSelector(self.llm_model)
        self.background_choice_selector = BackgroundChoiceSelector(self.llm_model)
        self.item_selector = ItemSelector(self.llm_model)

    def select_background_details(
        self, raw_background: Background, character_description: str
    ) -> tuple[Background, str]:
        for (
            target_field,
            source_field,
            count,
            description,
        ) in raw_background.get_items_to_select():
            kwargs = raw_background.model_dump(serialize_as_any=True)
            choices = kwargs[source_field]
            values = self.background_choice_selector.generate(
                character_description, description, choices, count
            )
            setattr(raw_background, target_field, values)
            character_description += f"\n {target_field}: {values} \n"
            print("Selected", target_field, values)
        return raw_background, character_description

    def generate(self, character_description: str) -> Background:
        background_type = self.background_selector.generate(character_description)
        print("Selected background:", background_type)

        raw_background = BACKGROUNDS[background_type]

        background_description = (
            f"\n Background: {background_type.value}: {raw_background.description} \n"
        )
        character_description += background_description

        raw_background, character_description = self.select_background_details(
            raw_background, character_description
        )

        print("Selecting tools")
        raw_background.tool_proficiencies = self.item_selector.generate(
            background_description,
            raw_background.tool_proficiencies,
            "Select tools that this character knows how to use based on the background. Only output instrument names.",
        )

        background_description += f"\n Known tools: {[item.name for item in raw_background.tool_proficiencies]} \n"
        print("Selecting equipment")
        raw_background.equipment = self.item_selector.generate(
            background_description,
            raw_background.equipment,
            "Select all items that this character should have based on the background and known tools. Only output item names.",
        )

        return raw_background
