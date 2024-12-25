from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class LoreGenerator:
    """
    Lore generator.
    It should create locations, geography, and history of the world.
    It creates a plan with set of steps for generating different entities for the Graph database.

    """

    LORE_STORY_PROMPT = """
You are a Dungeons and Dragons story master. 

-Goal- 
Describe the world for the One-Shot adventure.

-Steps-
- Define the area of the world, where the story takes place.
- Describe the locations in the area.
- Describe communities and their relationships.

-Constrains-
It should be easy to distinguish different entities mentioned in the story.
They all must have unique names and descriptions.
The world should be consistent and have a logical structure.

Output:
"""

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        lore_prompt = PromptTemplate.from_template(LoreGenerator.LORE_STORY_PROMPT)
        self.lore_chain = lore_prompt | llm_model | StrOutputParser()

    def generate(self):
        lore = self.lore_chain.invoke({})
        return lore
