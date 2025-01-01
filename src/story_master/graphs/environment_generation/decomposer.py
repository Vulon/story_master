import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.storage.map.map_model import Location


class LocationDecomposer:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Decompose a location into smaller locations.
    
    Your location should be somewhere inside the Coast of Swords.
    The time is the 15th Century DR.
    
    -Steps-
    1. Read the description of the larger location.
    2. Read the names of existing locations in the same are as the larger location for the context.
    3. Decompose the larger location into smaller locations.
        General areas like Faerûn have different regions like the Sword Coast.
        Regions have different settlements like Waterdeep.
        Settlements have different districts like the Dock Ward.
        Districts or small settlements have different buildings like the Friendly Inn.
        Don't output more than 5 smaller locations.
    4. Output the names of smaller locations in XML format in English.
        Format: <Location>First location</Location><Location>Second location</Location>        
        Don't output the parent location.
        All smaller locations should be on the same level and be smaller than the parent location.
    
    -Large location description-
    {location_description}
    
    -Neighbour large locations-
    {neighbour_locations}
    
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.pattern = re.compile(r"<Location>(.*)</Location>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[str]:
        matches = self.pattern.findall(output)
        return matches

    def generate(
        self, parent_location: Location, neighbour_location_names: list[str]
    ) -> list[str]:
        location_description = parent_location.description
        neighbour_locations = " ; ".join(neighbour_location_names)
        location_names = self.chain.invoke(
            {
                "location_description": location_description,
                "neighbour_locations": neighbour_locations,
            }
        )
        return location_names
