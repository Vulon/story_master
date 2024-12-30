from story_master.llm_client import get_client
from story_master.settings import Settings
from story_master.graphs.character_generation.character_generator import (
    CharacterGenerator,
)


class Engine:

    def __init__(self):
        settings = Settings()
        self.client = get_client()
        self.character_generator = CharacterGenerator(self.client)

    def run(self):
        character_description = "A tall, strong, and wise old man. His axe helped him escape many dire situations."

        generated_character = self.character_generator.generate(character_description)

        print(generated_character)
