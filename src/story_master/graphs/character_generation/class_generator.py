import re
from difflib import get_close_matches

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.entities.characteristics import SKILL_CONDITIONS, SkillType
from story_master.entities.classes import CLASSES, Class, ClassType
from story_master.utils.selection import SomeOf


class ClassSelector:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Identify the best game class for the character described.

    -Steps-
    1. Read the character description
    2. Identify the class that best fits the character's description.
    3. Output the name of the class in XML format.
       Example output: <Output>Class name</Output>

    -Available classes-
    {class_names}

    -Class descriptions-
    {class_descriptions}

    -Character description-
    {character_description}

    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.output_pattern = re.compile(r"<Output>(.*)</Output>")
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def create_short_class_descriptions(self) -> str:
        descriptions = []
        for class_type, class_object in CLASSES.items():
            description = (
                f"{class_type.value}: {class_object.get_short_class_description()}"
            )
            descriptions.append(description)
        return "\n".join(descriptions)

    def create_all_class_names(self) -> str:
        return "; ".join([class_type.value for class_type in CLASSES.keys()])

    def parse_output(self, output: str) -> ClassType:
        match = self.output_pattern.search(output)
        parsed_string = get_close_matches(
            match.group(1), [item.value for item in CLASSES.keys()]
        )[0]
        return ClassType(parsed_string)

    def generate(self, character_description: str) -> ClassType:
        class_names = self.create_all_class_names()
        class_descriptions = self.create_short_class_descriptions()
        class_type = self.chain.invoke(
            {
                "class_names": class_names,
                "class_descriptions": class_descriptions,
                "character_description": character_description,
            }
        )
        return class_type


class SkillSelector:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Select the skills for the character described.

    -Steps-
    1. Read the character description
    2. Read all available skills
    3. Read how many skills the character can choose
    4. Select the skills that best fit the character's description.
    5. Output the names of the selected skills in XML format.
        Every skill should be in a separate tag.
        Example output: <Output>Skill1</Output><Output>Skill2</Output>

    -Amount of skills to choose-
    {skills_amount}
        
    -Available skills-
    {skills_description}

    -Character description-
    {character_description}

    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.output_pattern = re.compile(r"<Output>(.*?)</Output>")
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[SkillType]:
        parsed_skills = []
        for raw_skill in self.output_pattern.findall(output):
            parsed_string = get_close_matches(
                raw_skill, [item.value for item in SKILL_CONDITIONS.keys()]
            )[0]
            parsed_skills.append(SkillType(parsed_string))
        return parsed_skills

    def create_skills_description(self, available_skills: list[SkillType]) -> str:
        descriptions = []
        for skill_type in available_skills:
            description = f"(Name: {skill_type.value} | description: {SKILL_CONDITIONS[skill_type]})"
            descriptions.append(description)
        return "\n".join(descriptions)

    def generate(
        self, character_description: str, class_object: Class, skills: SomeOf
    ) -> list[SkillType]:
        skills_description = self.create_skills_description(skills.items)
        return self.chain.invoke(
            {
                "skills_amount": skills.count,
                "skills_description": skills_description,
                "character_description": character_description,
            }
        )


class ClassGenerator:
    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.class_selector = ClassSelector(self.llm_model)
        self.skill_selector = SkillSelector(self.llm_model)

    def generate(self, character_description: str) -> Class:
        class_type = self.class_selector.generate(character_description)
        print("Selected class")
        print(class_type)
        class_object = CLASSES[class_type].model_copy()
        if isinstance(class_object.skills, SomeOf):
            skills = self.skill_selector.generate(
                character_description, class_object, class_object.skills
            )
            print("Selected skills")
            print(skills)
            class_object.skills = skills

        return class_object
