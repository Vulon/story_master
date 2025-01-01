from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.storage.map.map_model import Location


class InteriorGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Generate interior for a building or a location.
    
    -Steps-
    1. Read the description of the location that will contain the new interior.
        It can be a building, a dungeon, a cave, or any other location.
    2. Create a general design of the interior.
        Describe how large the interior is, where the entrance is, and what are the main features.
    3. Generate details for the interior.
        Describe the furniture, decorations, and any other objects that can be found inside.
        Describe the relative position of the objects.

    Write the text in the natural language. Don't use any XML tags.

    The description should be detailed enough to allow a player to navigate the interior.
    But keep it concise and don't include unnecessary details.
    
    -Location description-
    <Location>
    {location_description}
    </Location>
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser()

    def generate(self, location: Location) -> Location:
        location_description = f"{location.name}. {location.description}"
        interior_description = self.chain.invoke(
            {
                "location_description": location_description,
            }
        )
        location.interior = interior_description
        return location
