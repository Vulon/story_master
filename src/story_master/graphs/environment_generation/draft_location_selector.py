import re
from difflib import get_close_matches

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger


class LocationSelector:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Select a location from a list of locations that best suit the provided description or task.
    
    -Steps-
    1. Read the description of the location you need to select.
    2. Read the list of locations you can choose from.
    3. Select the location that best fits the description.
        Output the name of the location in XML format: <Location>Selected location</Location>
    
    -Location description-
    {location_description}
    
    -Locations to choose from-
    {locations}
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.pattern = re.compile(r"<Location>(.*)</Location>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> str:
        try:
            matches = self.pattern.search(output)
            return matches.group(1)
        except Exception as e:
            logger.error(f"LocationSelector. Failed to parse output: {output}")
            raise e

    def generate(self, location_names: list[str], location_description: str) -> str:
        locations = "\n".join(
            [f"<Location>{location}</Location>" for location in location_names]
        )
        selected_location = self.chain.invoke(
            {
                "location_description": location_description,
                "locations": locations,
            }
        )
        selected_location = get_close_matches(selected_location, location_names)[0]
        return selected_location
