import re


from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger


class CharacterDescriptionGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Write a description for a new character.
    
    -Steps-
    1. Read the location description.
    2. Read the intent for the action. It should give you an idea of the character's role.
    3. Write a description for the character.
        Description will be used to generate a new character. 
        It should describe, how character looks, what is his/her background, etc.
        A character in general can be a commoner, a merchant, an adventurer, a creature, etc.
    4. Output the description in XML format.
        Example output: <Output>New character description</Output>
        
    -Location  description-  
    {location_description}
    
    -Intent-
    {intent}
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.output_pattern = re.compile(r"<Output>(.*?)</Output>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> str:
        try:
            output = output.replace("\n", " ").strip()
            match = self.output_pattern.search(output)
            return match.group(1)
        except Exception as e:
            logger.error(
                f"CharacterDescriptionGenerator. Failed to parse output: {output}"
            )
            raise e

    def generate(self, intent: str, location_description: str) -> str:
        character_description = self.chain.invoke(
            {"intent": intent, "location_description": location_description}
        )
        return character_description
