import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger
from story_master.storage.map.map_model import LargeArea


class LocationDecomposer:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Decompose a location into smaller locations.
    
    Game map follows the tree structure, where the larger location is decomposed into smaller locations.
    Your location should be somewhere inside the Coast of Swords.
    
    -Steps-
    1. Read the description of the larger location.
    2. Read the location tree hierarchy. It describes the relations from larger location all the way down to the current location
    3. Decompose the larger location into smaller locations.
        General areas like Faerûn have different regions like the Sword Coast.
        Regions have different settlements like Waterdeep.
        Large settlements have different districts or wards.
        Districts or small settlements have different buildings like taverns, shops, etc.
        Don't output more than 5 smaller locations.
        Don't decompose buildings into rooms, except for large buildings like castles.
        Don't output the name of any location already present in the location tree hierarchy.
    4. Output the names of smaller locations in XML format
        Format: <Location>First location</Location><Location>Second location</Location>
        All smaller locations should be on the same level and be smaller than the parent location.
    All names should be in English
    
    -Large location description-
    {location_description}
    
    -Location tree hierarchy-
    {location_tree}    
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.pattern = re.compile(r"<Location>(.*)</Location>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[str]:
        try:
            matches = self.pattern.findall(output)
            return matches
        except Exception as e:
            logger.error(f"LocationDecomposer. Failed to parse output: {output}")
            raise e

    def generate(
        self, parent_location: LargeArea, location_tree_path: list[LargeArea]
    ) -> list[str]:
        location_description = parent_location.description
        tree_path_names = [location.name for location in location_tree_path]
        location_tree_string = " -> ".join(tree_path_names)
        location_names = self.chain.invoke(
            {
                "location_description": location_description,
                "location_tree": location_tree_string,
            }
        )
        location_names = [
            name for name in location_names if name not in tree_path_names
        ]
        return location_names
