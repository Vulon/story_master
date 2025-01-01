import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.storage.map.map_model import Location


class LocationGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Generate all fields for a Location object.
    
    -Steps-
    1. Read the description of the parent location that will contain the new location.
    2. Read the name of the location you need to generate.
    3. Generate the description of the location.
        Output the description in XML tags: <Description>Generated description</Description>
    4. Generate the short description of the location.
        Output the short description in XML tags: <ShortDescription>Generated short description</ShortDescription>
        Short description should be one or two sentences long.
    5. Output a flag that indicates if the location can be further decomposed.
        The smallest location should be of similar size to a building.
        Output the flag in XML tags: <IsLeaf>True</IsLeaf> or <IsLeaf>False</IsLeaf>
        
    Don't create nested tags.
    Write in English only.
    
    -Example-
    Example for the location "The Sword Coast":
    <Description>
The Sword Coast is the region in western Faerûn that lay along the coast of the Sea of Swords and extends inward into to the vale.
The Sword Coast was an expansive tract of wilderness, dotted with independent cities and overrun by bands of monstrous creatures,
that some saw as merely a place through which you had to travel in order to reach an actual meaningful destination.
It was much more than that of course, a rich and vibrant land with a long and storied history that encompassed some of the most important cities in all the Realms.
    </Description>
    <ShortDescription>The Sword Coast is the region in western Faerûn. It's a rich and vibrant land with wild monsters and important cities</ShortDescription>
    <IsLeaf>False</IsLeaf>
    
    -Parent location description-
    {parent_location_description}
    
    -Location name-
    {location_name}
    
    Output:    
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.description_pattern = re.compile(r"<Description>(.*)</Description>")
        self.short_description_pattern = re.compile(
            r"<ShortDescription>(.*)</ShortDescription>"
        )
        self.is_leaf_pattern = re.compile(r"<IsLeaf>(.*)</IsLeaf>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> tuple[str, str, bool]:
        output = output.replace("\n", " ")
        description_match = self.description_pattern.search(output)
        short_description_match = self.short_description_pattern.search(output)
        is_leaf_match = self.is_leaf_pattern.search(output)
        description = description_match.group(1)
        short_description = short_description_match.group(1)
        is_leaf = is_leaf_match.group(1).lower() == "true"
        return description, short_description, is_leaf

    def generate(
        self, parent_location: Location, new_location_name: str, max_id: int
    ) -> Location:
        description, short_description, is_leaf = self.chain.invoke(
            {
                "parent_location_description": parent_location.description,
                "location_name": new_location_name,
            }
        )
        new_location = Location(
            id=max_id + 1,
            name=new_location_name,
            description=description,
            short_description=short_description,
            parent_location=parent_location.id,
            is_leaf=is_leaf,
        )
        return new_location
