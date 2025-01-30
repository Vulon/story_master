import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.storage.storage_models import Sim
from story_master.storage.storage_manager import StorageManager
from story_master.log import logger


class ObservationAgent:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Create a memory entry for the character.    

    -Steps-
    1. Read the description of the location.
    2. Read the description of the character.
    3. Read the character's memories.
    4. Read the character's situation.
    5. Read the context.
    6. Create a memory entry for the character:
        Memory entry should contain a title, content and importance score.
        Title: Title of the memory entry. A short sentence describing this event.
        Content: Content of the memory entry about current situation. A detailed description of the event.
        Importance: Importance of the memory entry. A number between 1 and 10.
    7. Output memory entry in XML format.
        Format: <Title>Title</Title>
                <Content>Content</Content>
                <Importance>Importance</Importance>
    8. Update character's status: 
        Read existing character situation and update it with the new information.
        Output the new character situation in XML format.
        Format: <CharacterStatus>Character situation</CharacterStatus>
    
    -Location description-
    {location_description}
    
    -Character description-
    {character_description}
    
    -Character memories-
    {character_memories}
    
    -Character situation-
    {character_situation}
    
    -Context-
    {context}

    ########
    Output:
    """

    def __init__(
        self,
        storage_manager: StorageManager,
        llm_model: BaseChatModel,
    ):
        self.storage_manager = storage_manager
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.title_pattern = re.compile(r"<Title>(.*?)</Title>")
        self.content_pattern = re.compile(r"<Content>(.*?)</Content>")
        self.importance_pattern = re.compile(r"<Importance>(.*?)</Importance>")
        self.status_pattern = re.compile(r"<CharacterStatus>(.*?)</CharacterStatus>")
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> tuple[str, str, int, str | None]:
        try:
            output = output.replace("\n", " ")
            title = self.title_pattern.search(output).group(1)
            content = self.content_pattern.search(output).group(1)
            importance = int(self.importance_pattern.search(output).group(1))
            status_match = self.status_pattern.search(output)
            status_description = status_match.group(1) if status_match else None
            return title, content, importance, status_description
        except Exception as e:
            logger.error(f"ObservationAgent. Failed to parse output: {output}")
            raise e

    def format_character_description(self, sim: Sim) -> str:
        lines = [
            f"ID: {sim.id}. ",
            f"Name: {sim.character.name}. ",
            f"Type: {sim.character.type}. ",
        ]
        return " ".join(lines)

    def run(
        self,
        sim: Sim,
        context: str,
        memories_string: str = "",
        location_description: str = "",
    ) -> None:
        character_situation = sim.current_status or ""
        character_description = self.format_character_description(sim)
        title, content, importance, status_description = self.chain.invoke(
            {
                "location_description": location_description,
                "character_description": character_description,
                "character_memories": memories_string,
                "character_situation": character_situation,
                "context": context,
            }
        )
        if status_description:
            sim.current_status = status_description

        self.storage_manager.add_observation(title, content, importance, sim)
