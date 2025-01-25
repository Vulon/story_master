import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.entities.character import CharacterType
from story_master.storage.storage_models import Sim
from story_master.storage.memory.memory_model import Observation
from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent


class CharacterIdentifier:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Identify who the character is talking to.
    
    -Steps-
    1. Read the description of characters in this location. 
    2. Read the description of the character who is talking.
    3. Read the memory of the character who is talking.
    4. Read the intention of the character who is talking.
    5. Identify the dialog responder, who the main character is talking to.
    6. Output the ID of the dialog responder.
        Format: <Responder>ID</Responder>
        
    -Main character intention-
    {main_character_intention}     
    
    -Main character description-
    {main_character_description}
    
    -Main character memory-
    {main_character_memory}    
    
    -Characters description-
    {characters_description}
    
    ########
    Output:    
    """

    def __init__(self, llm_model: BaseChatModel):
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.responder_pattern = re.compile(r"<Responder>(.*?)</Responder>")
        self.chain = self.prompt | llm_model | StrOutputParser()

    def parse_output(self, output: str, sims: list[Sim]) -> Sim:
        responder_match = self.responder_pattern.search(output)
        responder_id = int(responder_match.group(1))
        responder = [sim for sim in sims if sim.id == responder_id][0]
        return responder

    def format_memories(self, memories: list[Observation]) -> str:
        strings = []
        for memory in memories:
            strings.append(f"{memory.title}: {memory.content}")
        memories_string = "<Memories>" + "; ".join(strings) + "</Memories>"
        return memories_string

    def format_character(self, id: int, sim: Sim) -> str:
        return f"(ID: {id}. Name: {sim.character.name}. Status: {sim.current_status})"

    def format_characters(self, sims: list[Sim]) -> str:
        strings = []
        for sim in sims:
            strings.append(self.format_character(sim.id, sim))
        characters_string = "<Characters>" + "; ".join(strings) + "</Characters>"
        return characters_string

    def run(
        self,
        main_sim: Sim,
        main_character_intention: str,
        sims: list[Sim],
        memories_string: str,
        character_description: str,
    ) -> Sim:
        sims = [sim for sim in sims if sim.id != main_sim.id]
        characters_description = self.format_characters(sims)
        raw_output = self.chain.invoke(
            {
                "characters_description": characters_description,
                "main_character_intention": main_character_intention,
                "main_character_description": character_description,
                "main_character_memory": memories_string,
            }
        )
        responder = self.parse_output(raw_output, sims)
        return responder


class DialogAgent:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Generate a response in a dialog between the main character and a dialog responder.
    
    -Steps-
    1. Read the main character intention.
    2. Read the description of the main character
    3. Read main character memory.
    4. Read the description of the dialog responder.
    5. Read the memory of the dialog responder.
    6. Read the description of the location.
    7. Generate a response from the perspective of the dialog responder.
    8. Output the response:
        Format: <Response>Response</Response>
    
    -Main character intention-
    {main_character_intention}
    
    -Main character description-
    {main_character_description}
    
    -Main character memory-
    {main_character_memory}
    
    -Dialog responder description-
    {dialog_responder_description}
    
    -Dialog responder memory-
    {dialog_responder_memory}
    
    -Location description-
    {location_description}
    
    ########
    Output:
    """

    def __init__(
        self,
        llm_model: BaseChatModel,
        storage_manager: StorageManager,
        summary_agent: SummaryAgent,
    ):
        self.storage_manager = storage_manager
        self.summary_agent = summary_agent
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.pattern = re.compile(r"<Response>(.*?)</Response>")
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output
        self.character_identifier = CharacterIdentifier(llm_model)

    def parse_output(self, output: str) -> str:
        print("Dialog output", output)
        output = output.replace("\n", " ")
        match = self.pattern.search(output)
        return match.group(1)

    def format_character_description(self, sim: Sim) -> str:
        lines = [
            f"ID: {sim.id}. ",
            f"Name: {sim.character.name}. ",
            f"Status: {sim.current_status}. ",
            f"Type: {sim.character.type}. ",
            f"Sex: {sim.character.sex}. ",
            f"Alignment: {sim.character.alignment}. ",
            f"Race: {sim.character.race.name}. ",
        ]
        if sim.character.type == CharacterType.ADVENTURER:
            lines.append(f"Class: {sim.character.klass.name}. ")
            lines.append(f"Background: {sim.character.background.get_description()}. ")
        return " ".join(lines)

    def run(
        self,
        main_sim: Sim,
        main_character_intention: str,
        memories_string: str,
        character_description: str,
        location_description: str,
    ) -> tuple[str, Sim]:
        location = self.storage_manager.get_location(main_sim.current_location_id)
        location_characters = self.storage_manager.get_location_characters(location)

        responder = self.character_identifier.run(
            main_sim,
            main_character_intention,
            location_characters,
            memories_string,
            character_description,
        )

        dialog_responder_description = self.summary_agent.summarize_character(
            f"{responder.character.name} is responding to {main_sim.character.name}, who is saying: {main_character_intention}",
            responder.character,
        )
        responder_memories = self.storage_manager.get_memories(
            f"{main_sim.character.name} is saying: {main_character_intention}",
            responder,
        )
        dialog_responder_memory = self.summary_agent.summarize_memories(
            f"{responder.character.name} is responding to {main_sim.character.name}, who is saying: {main_character_intention}",
            responder_memories,
        )

        response = self.chain.invoke(
            {
                "main_character_intention": main_character_intention,
                "main_character_description": character_description,
                "main_character_memory": memories_string,
                "dialog_responder_description": dialog_responder_description,
                "dialog_responder_memory": dialog_responder_memory,
                "location_description": location_description,
            }
        )
        return response, responder
