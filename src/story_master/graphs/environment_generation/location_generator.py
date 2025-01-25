import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger

from story_master.storage.map.map_model import LargeArea, DetailedArea


class LocationGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Generate a new location
    
    The game world is divided into locations. Location follow tree structure, where the parent location contains smaller locations.
    Write in English only.
        
    -Steps-
    1. Read the description of the parent location that will contain the new location.
    2. Read the name of the location you need to generate.
    3. Generate the description of the location.
        Output the description in XML tags: <Description>Generated description</Description>
        The description should be detailed, about 1-2 paragraphs long, like a wiki introduction.        
    4. Output a flag that indicates if the location can be further decomposed.
        The smallest location can be a building, or a small area. 
        The small location can't be decomposed further, it will follow a different logic. 
        The smallest location will have a 2D grid structure with detailed objects, like furniture, trees, rocks, etc. 
        Output the flag in XML tags: 
        <Smallest>True</Smallest> - meaning the location can't be decomposed further 
        <Smallest>False</Smallest> - meaning the location can be decomposed further
            
    -Parent location description-
    {parent_location_description}
    
    -Location name-
    {location_name}
    
    -Output structure-
    <Description>Generated description</Description>
    <Smallest>True</Smallest> or <Smallest>False</Smallest>
    
    Output:    
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.description_pattern = re.compile(r"<Description>(.*?)</Description>")
        self.decomposible_pattern = re.compile(r"<Smallest>(.*?)</Smallest>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> tuple[str, bool]:
        try:
            output = output.replace("\n", " ")
            description_match = self.description_pattern.search(output)
            decomposible_match = self.decomposible_pattern.search(output)

            description = description_match.group(1)
            decomposible = decomposible_match.group(1).lower() == "false"
            return description, decomposible
        except Exception as e:
            logger.error(f"LocationGenerator. Failed to parse output: {output}")
            raise e

    def generate(
        self, parent_location: LargeArea, new_location_name: str, area_id: int
    ) -> LargeArea | DetailedArea:
        description, decomposible = self.chain.invoke(
            {
                "parent_location_description": parent_location.description,
                "location_name": new_location_name,
            }
        )
        if decomposible:
            new_location = LargeArea(
                id=area_id,
                name=new_location_name,
                description=description,
                parent_location=parent_location.id,
            )
        else:
            new_location = DetailedArea(
                id=area_id,
                name=new_location_name,
                description=description,
                parent_location=parent_location.id,
            )
        return new_location
