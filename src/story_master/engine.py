from story_master.logic.lore_generator import LoreGenerator
from story_master.logic.story_generator import StoryGenerator
from story_master.memory.database_manager import DatabaseManager
from story_master.llm_client import get_client
from story_master.settings import Settings
from story_master.logic.entity_parser import EntityFinder, EntityParser

TEST_STORY = """
### Adventure Plot

In the heart of Aelgarath, an ancient continent shrouded in legend and mystery, the people of Alveria are facing their greatest challenge yet. The Eldrid Dominion has been attacked by a horde of orcs who have grown bolder with each passing day, pillaging villages and terrorizing small settlements across the Wildlands. This sudden assault has disrupted the balance of power within Aelgarath.

The Eldrid Dominion’s magical protections are failing against the sheer force and ferocity of the invading orcs. The only hope lies in an ancient artifact known as the **Scepter of Light**, said to be able to repel dark forces and banish evil spirits. This scepter is rumored to have been created by an elven high mage who was tasked with safeguarding it from those who would misuse its power.

However, the scepter’s whereabouts are unknown, and only a select few possess knowledge of where it might be hidden. The orcs’ relentless advance demands immediate action, and Alveria is calling for brave adventurers to embark on this perilous journey: find the Scepter of Light, stop the orcs, and restore peace.

### Main Characters

**Characters**
- **Aelara**: A wise and powerful elven high mage living in Sage's Grove. She has intimate knowledge of the Eldrid Dominion’s location but lacks a clear path to the scepter.
- **Vossar**: The leader of Ironclad Fortresses, known for his tactical genius and unwavering loyalty. He will provide military support if you are able to gather allies.
- **Lylea**: A former thief turned bard with uncanny skills in gathering information from whispers found within the Wildlands. Her charm often proves useful in gaining insight into ancient places.
- **Ragnar**: The head of the Eldrid Dominion, a charismatic and resourceful elven leader who is eager to protect his people but lacks experience dealing with orcs.

### Main Goal

To find the Scepter of Light within the span of two days. You will travel through enchanted forests, across rugged terrains, and up mountain peaks, ultimately reaching its rumored location hidden deep in an ancient magic well that has never been disturbed by human hands.

### Problems to Face

1. **Magical Wraiths**: As you venture deeper into the Wildlands, supernatural entities known as wraiths start to manifest. These ethereal beings feed on fear and have a habit of following adventurers who disturb their natural balance.
2. **Vampires of the Blackwood Forest**: Hidden within the Forest of Echoes lies a group of vampires preying on travelers for sustenance. They are heavily fortified, making it dangerous to enter without preparation.
3. **Orc Bandits in Plain Sight**: While your primary target is the Scepter, you will also need to fend off orc bandit groups who patrol their territory between raids. Their leaders can be bribed or outsmarted to get past them safely.

### Conclusion

Each character brings unique skills and strengths to the table: Aelara’s magical prowess, Vossar’s military strategy, Lylea’s ability to gather information, and Ragnar’s leadership. Together, they form a formidable team capable of overcoming obstacles that stand between you and the Scepter of Light. But be wary – there are many dangers along this journey, and only by working together can you succeed in your quest.


"""


class Engine:
    """
    The main game engine that runs the game.
    It should call different logic classes and handle the game state.
    It should load and save entities from the graph database.
    """

    def __init__(self):
        settings = Settings()
        self.client = get_client()
        self.lore_generator = LoreGenerator(self.client)
        self.story_generator = StoryGenerator(self.client)
        self.db_manager = DatabaseManager()
        self.entity_finder = EntityFinder(self.client)
        self.entity_parser = EntityParser(self.client)

    def run(self):
        print("Generating steps")
        steps = self.story_generator.generate_steps(TEST_STORY)
        print("Steps")
        print(steps)

        return

        lore = self.lore_generator.generate()
        print("Lore")
        print(lore)

        # loaded_entities = self.db_manager.load_entities(entities)
        story = self.story_generator.generate_story(lore)
        print()
        print()
        print("_" * 40)
        print("Story")
        print(story)
        print()
        print("_" * 40)

        steps = self.story_generator.generate_steps(TEST_STORY)
        print()
        print(steps)
        print()
        print("_" * 40)
        # entities = self.entity_finder.run(story)
        # print()
        # print()
        # print("Entities")
        # print(entities)
        # for entity_type in entities:
        #     if entity_type == "Location":
        #         continue
        #     for entity_name in entities[entity_type]:
        #         print()
        #         print()
        #         print()
        #         print("Entity parser input")
        #         print(entity_type, entity_name)
        #         entity_json = self.entity_parser.run("", story, entity_type, entity_name)
        #         print("Parsed json")
        #         print(entity_json)
