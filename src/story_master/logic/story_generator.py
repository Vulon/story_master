from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from story_master.memory.registry import ENTITY_REGISTRY, RELATION_REGISTRY


class StoryGenerator:
    """
    Story generator.
    It should create a story for the players to explore.
    """

    STORY_PROMPT = """
You are a Dungeons and Dragons story master. 

-Goal-
Write a story for the One-Shot adventure.

-Steps-
Use the world details provided to you. 
Create a main goal of the adventure for the DnD One-Shot session. 
Describe all problems players will face. 
Describe all characters in the story that are important for the adventure.
Clearly define the main villain and their motivations. 

###########
-World details-
<world details>
{lore}
</world details>
###########
Output:
"""

    STEPS_PROMPT = """
You are a Dungeons and Dragons story master. 

-Goal-
Write steps required to create all entities and relations for the story.

-Steps-
- Idenfity all entities, that are mentioned in the story.
  You will have a complete list of entity types that you can use.
- Idenfity all relations between entities.
  You will have a complete list of relation types that you can use.
- Output all entities in the following format:
  <Entity>Entity type: Entity name</Entity>
  The entity type should be exactly the same as in the provided list.
- Output all relations in the following format:
  <Relation>Relation type: Entity name 1 -> Entity name 2</Relation>
Output every entity and relation in a separate line.

-Entities list-
<Entities list>{entities}</Entities list> 

-Relations list-
<Relations list>{relations}</Relations list>

###########
-Story-
<story>
 {story}
</story>
###########
Output:
"""

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        story_prompt = PromptTemplate.from_template(StoryGenerator.STORY_PROMPT)
        self.story_chain = story_prompt | llm_model | StrOutputParser()
        steps_prompt = PromptTemplate.from_template(StoryGenerator.STEPS_PROMPT)
        self.steps_chain = steps_prompt | llm_model | StrOutputParser()

    def generate_story(self, lore: str) -> str:
        story = self.story_chain.invoke({"lore": lore})
        return story

    def _create_entities_list(self) -> str:
        output_list = []
        for entity_name, entity_class in ENTITY_REGISTRY.items():
            output_list.append(
                f"<Entity Type>{entity_name}: {entity_class.get_class_description()}</Entity Type>"
            )
        return "\n".join(output_list)

    def _create_relations_list(self) -> str:
        output_list = []
        for relation_name, relation_class in RELATION_REGISTRY.items():
            output_list.append(
                f"<Relation Type>{relation_name}: {relation_class.get_class_description()}</Relation Type>"
            )
        return "\n".join(output_list)

    def generate_steps(self, story: str) -> str:
        entities = self._create_entities_list()
        relations = self._create_relations_list()
        steps = self.steps_chain.invoke(
            {"story": story, "entities": entities, "relations": relations}
        )
        return steps
