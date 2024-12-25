from story_master.memory.registry import ENTITY_REGISTRY
from story_master.memory.entity import Entity
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
import json


class EntityFinder:
    PROMPT = """
You are a Dungeons and Dragons assistant. 

-Goal-
Identify all characters and locations in the provided text.

-Steps-
1. Find all entities of the provided types in the text
2. Write the entity type exactly as provided in the list
3. Write the unique name for each entity
4. Output each unique entity with its type and name

-List of entity types-
{entity_types}

-Examples-
##########
EXAMPLE 1:
In the bustling town of Riverkeep, Bork Short-tempered lowered his Oak club.
The settlement, protected by stone walls, served as a haven for travelers.
As night fell, Bork met with Elara Swiftfoot at the Golden Duck Inn to discuss their next adventure into the Whispering Woods.
#########
Output:
[
    (Character, Bork Short-tempered),    
    (Location, Riverkeep),
    (Location, Golden Duck Inn),
    (Location, Whispering Woods),
    (Character, Elara Swiftfoot)
]
#########
REAL DATA
#########
{text}
#########
Output:
"""

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt_template = PromptTemplate.from_template(EntityFinder.PROMPT)
        self.chain = prompt_template | llm_model | StrOutputParser() | self.parse_output

    @staticmethod
    def parse_output(text: str) -> dict[str, list[str]]:
        string_tuples = re.findall(r"\(.*?\)", text)
        print("parsing output: ", text)
        string_tuples = [item[1:-1].split(",") for item in string_tuples]
        true_keys = set(ENTITY_REGISTRY.keys())
        entity_name_tuples = [
            (item[0], item[1]) for item in string_tuples if item[0] in true_keys
        ]
        print("entity_name_tuples:", entity_name_tuples)
        entity_table = dict()
        for entity_type, entity_name in entity_name_tuples:
            names_list = entity_table.get(entity_type, [])
            names_list.append(entity_name)
            entity_table[entity_type] = names_list

        return entity_table

    def _create_entity_registry_string(self) -> str:
        descriptions = []
        for entity_name, entity_class in ENTITY_REGISTRY.items():
            class_description = (
                f"(<{entity_name}>: {entity_class.get_class_description()})"
            )
            descriptions.append(class_description)
        print("Entity classes:", descriptions)
        return " ; ".join(descriptions)

    def run(self, text: str):
        output = self.chain.invoke(
            {"text": text, "entity_types": self._create_entity_registry_string()}
        )
        return output


class EntityParser:
    PROMPT = """
You are a Dungeons and Dragons assistant. 

-Goal-
Generate an entity from the provided text with all relevant fields.

-Steps-
- Find the entity of the specified type and name in the text.
  If this entity already exists in the database, you will see the context. Otherwise, it will be empty.
- Create a new entity with all required fields. 
  You must use the provided entity schema.
  You must use all information about this entity from the text. 
  If some information is missing, you should improvise, so that the entity is consistent with the world.
- Output the entity in the JSON format.

-Entity schema-
{entity_description}

-Example-
##########
<context></context>
<name>Bran</name>
<text>Bran, a sturdy dwarf with a long braided beard, is known for his bravery in battle.
He has a scar over his left eye from a fierce fight with an orc.
Despite his rough exterior, Bran is kind-hearted and always ready to help those in need.
He currently resides in the bustling town of Riverkeep.</text>
##########
Output:
{{
    "name": "Bran",
    "description": "Bran, a sturdy dwarf with a long braided beard, is known for his bravery in battle. Despite his rough exterior, Bran is kind-hearted",
    "race": "dwarf",
    "current_health": 15
}}

##########
REAL DATA
##########
<context>{context}</context>
<name>{name}</name>
<text>{text}</text>

##########
Output:
"""

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt_template = PromptTemplate.from_template(EntityParser.PROMPT)
        self.chain = prompt_template | llm_model | StrOutputParser() | self.parse_output

    def _create_entity_description(self, entity_type: str) -> str:
        entity_class = ENTITY_REGISTRY[entity_type]
        output = f"{entity_type}: {entity_class.get_fields_description()}"
        return output

    def parse_output(self, text: str):
        text = text.replace("\n", " ")
        match = re.search(r"\{.*?\}", text)
        print("parser match", match)
        json_string = match.group()
        json_object = json.loads(json_string)
        print("json_list", json_object)
        return json_object

    def run(
        self, context: str, text: str, entity_type: str, entity_name: str
    ) -> Entity:
        json_object = self.chain.invoke(
            {
                "text": text,
                "context": context,
                "entity_description": self._create_entity_description(entity_type),
                "name": entity_name,
            }
        )
        output = ENTITY_REGISTRY[entity_type](**json_object)
        return output
