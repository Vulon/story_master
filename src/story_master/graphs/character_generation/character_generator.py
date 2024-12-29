from langchain_core.language_models.chat_models import BaseChatModel
from story_master.graphs.character_generation.race_generator import RaceGenerator
from story_master.graphs.character_generation.class_generator import ClassGenerator


class CharacterGenerator:
    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.race_generator = RaceGenerator(self.llm_model)
        self.class_generator = ClassGenerator(self.llm_model)

    def generate(self, character_description: str):
        race = self.race_generator.generate(character_description)
        character_description += f"\n Race: {race.get_full_description()} \n"
        class_object = self.class_generator.generate(character_description)

        return class_object
