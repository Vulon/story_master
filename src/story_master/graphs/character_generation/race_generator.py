from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from story_master.entities.races import RaceType, RACES, Race
import re
from difflib import get_close_matches


output_pattern = re.compile(r"<Output>(.*)</Output>")


class RaceGenerator:

    PROMPT = """
You are a Dungeons and Dragons agent.

-Goal-
Identify the best game race for the character described.

-Steps-
1. Identify the race that best fits the character's description.
2. Output the name of the race in XML format.

-Available races-
{races_description}

-Output example-
<Output>Goblin</Output>

-Character description-
{character_description}

Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def generate(self, character_description: str) -> Race:
        races_description = self.create_races_description()
        print("Running generations")
        race_type = self.chain.invoke(
            {
                "races_description": races_description,
                "character_description": character_description,
            }
        )
        return RACES[race_type].model_copy()

    def parse_output(self, output: str) -> RaceType:
        match = output_pattern.search(output)
        parsed_string = get_close_matches(
            match.group(1), [item.value for item in RACES.keys()]
        )[0]
        return RaceType(parsed_string)

    def create_races_description(self) -> str:
        descriptions = []
        for race in RACES.values():
            descriptions.append(race.get_full_description(include_names=False))
        return "\n".join(descriptions)
