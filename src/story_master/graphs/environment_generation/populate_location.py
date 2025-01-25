import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger
from story_master.storage.storage_models import Sim


class LocationPopulationManager:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Design characters for the location.
    
    -Steps-
    1. Read the description of the location.
    2. Read the list of character already present in location if they exist.
    3. Design characters for the location.
       You need to create short 2-3 sentence descriptions for each character.
       No need for details like name, age, etc unless it is relevant.
       Describe who the character is.
       The character should be a single person.       
    4. Output the descriptions of the characters in XML format.
        Format: <Character>Character description</Character>
        Output every character in a separate line.
        Don't output more than 5 characters.
        
    Create only commoner and merchant characters.
    
    -Location description-
    {location_description}
    
    -Characters already present-
    {characters_description}
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.pattern = re.compile(r"<Character>(.*?)</Character>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[str]:
        try:
            matches = self.pattern.findall(output)
            return matches
        except Exception as e:
            logger.error("LocationPopulationManager. Error parsing output: output")
            raise e

    def generate(
        self, location_description: str, location_sims: list[Sim]
    ) -> list[str]:
        character_lines = []
        for sim in location_sims:
            character_description = f'{sim.character.name}: {sim.character.type}, Status: {sim.current_status or "Not defined"}'
            character_lines.append(character_description)
        characters_description = " ; ".join(character_lines)

        generated_character_descriptions = self.chain.invoke(
            {
                "location_description": f"<Location>{location_description}</Location>",
                "characters_description": f"<Characters>{characters_description}</Characters>",
            }
        )
        return generated_character_descriptions
