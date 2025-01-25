from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
import re
from story_master.storage.map.map_model import EnvironmentPart
from story_master.utils.selection import get_batched
from story_master.log import logger


# Create a list of possible objects that can be generated in a location.
# Create an empty 2D grid.
# Split the grid into chunks.
# Generate objects for each chunk.

ENVIRONMENT_PART_GENERATION_BATCH_SIZE = 5

DEFAULT_GRID_SIZE = 16


class ObjectNamesGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Create a list of all objects that can be generated in a location.
    
    -Steps-
    1. Read the description of the location.
    2. Think of all objects that can be generated in the location.
        An object can be a tree, a chest, a bed, a rock, a book, etc. 
        Types of objects depend on the location.
        You can be creative and add some objects that are not typical for the location, but make sense in the context.
    3. Write down the names of all objects.
        Output the names in a comma-separated list.
        Example: tree, chest, bed, rock, book
        
    -Location description-
    {location_description}
    
    -Output format-
    Format: first object name, second object name, ...
    
    Output only new object names separated with a comma.

    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[str]:
        try:
            output = output.replace("\n", " ")
            return [item.strip() for item in output.split(", ")]
        except Exception as e:
            logger.error(f"ObjectNamesGenerator. Failed to parse output: {output}")
            raise e

    def generate(self, location_description: str) -> list[str]:
        object_names = self.chain.invoke({"location_description": location_description})
        return object_names


class ObjectGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Generate objects for a location.
    
    The location is represented as a 2D grid. 
    Every cell in the grid can contain several objects. 
    A single object can occupy several cells.
    A single cell has a size of 1x1 meters.
    
    -Steps-
    1. Read the description of the location.
    2. Read the list of objects that you need to generate.
    3. For every object name generate the object. 
        Every object has the following properties:
        name: str - the name of the object
        description: str - a detailed description of the object
        dimensions: tuple[int, int] - the size of the object in the 2D grid in meters. The smallest object has dimensions of 1x1 meters.
    
    -Location description-
    {location_description}
    
    -Object names-
    {object_names}
    
    -Output format-
    (object_name, object_description, width, length),
    (object_name, object_description, width, length)
    
    Output every object on a separate line. Objects should be separated by a comma and enclosed in parentheses.
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.object_pattern = re.compile(r"\((.*?)\)")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[tuple[str, str, int, int]]:
        try:
            output = output.replace("\n", " ")
            raw_objects = self.object_pattern.findall(output)
        except Exception as e:
            logger.error(f"ObjectGenerator. Failed to parse output: {output}")
            raise e
        objects = []
        for raw_object in raw_objects:
            try:
                text_items = raw_object.split(",")
                name = text_items[0].strip()
                length = text_items[-1]
                width = text_items[-2]
                description = ",".join(text_items[1:-2]).strip()
                objects.append((name, description, int(width), int(length)))
            except Exception:
                logger.error(f"ObjectGenerator. Failed to parse object: {raw_object}")
                continue
        return objects

    def generate(
        self, location_description: str, object_names: list[str]
    ) -> list[EnvironmentPart]:
        raw_objects = []
        for object_names_batch in get_batched(
            object_names, ENVIRONMENT_PART_GENERATION_BATCH_SIZE
        ):
            object_names_str = ", ".join(object_names_batch)
            raw_objects_batch = self.chain.invoke(
                {
                    "location_description": location_description,
                    "object_names": object_names_str,
                }
            )
            raw_objects.extend(raw_objects_batch)
        objects = []
        for i, values in enumerate(raw_objects):
            name, description, width, length = values
            objects.append(
                EnvironmentPart(
                    id=i,
                    name=name,
                    description=description,
                    position=(0, 0),
                    dimensions=(width, length),
                )
            )
        return objects


class GridPlacer:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Place objects in a 2D grid.
    
    -Steps-
    1. Read the description of the location
    2. Read the list of objects that you can place
    3. Read the size of the 2D grid
    4. Place objects in the grid
        Every object can occupy several grid cells.
        One cell can contain several objects.
    5. Output the list of objects with their positions in the grid.
    
    -Location description-
    {location_description}
    
    -Available objects-    
    {objects}
    
    -Grid size-
    {grid_size}
    
    -Output format-
    Format: (object id, x, y), (object id, x, y), ...
    Where object id, x and y are integers.
    
    Output:    
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.object_pattern = re.compile(r"\((.*?)\)")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[tuple[int, int, int]]:
        try:
            output = output.replace("\n", " ")
            raw_objects = self.object_pattern.findall(output)
        except Exception as e:
            logger.error(f"GridPlacer. Failed to parse output: {output}")
            raise e
        objects = []
        for raw_object in raw_objects:
            try:
                object_id, x, y = raw_object.split(",")
                objects.append((int(object_id), int(x), int(y)))
            except Exception:
                logger.error(f"GridPlacer. Failed to parse object: {raw_object}")
                continue
        return objects

    def generate(
        self, location_description: str, objects: list[EnvironmentPart]
    ) -> list[EnvironmentPart]:
        objects_str = " ; ".join(
            [
                f"(ID: {obj.id}, Name: {obj.name}, Dimensions: {obj.dimensions[0]} x {obj.dimensions[1]})"
                for obj in objects
            ]
        )
        objects_table = {obj.id: obj for obj in objects}

        raw_object_values = self.chain.invoke(
            {
                "location_description": location_description,
                "objects": objects_str,
                "grid_size": f"{DEFAULT_GRID_SIZE} x {DEFAULT_GRID_SIZE}",
            }
        )
        objects = []
        for object_id, x, y in raw_object_values:
            obj = objects_table[object_id]
            objects.append(
                EnvironmentPart(
                    id=obj.id,
                    name=obj.name,
                    description=obj.description,
                    position=(x, y),
                    dimensions=obj.dimensions,
                )
            )
        return objects


class InteriorManager:
    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.object_names_generator = ObjectNamesGenerator(llm_model)
        self.object_generator = ObjectGenerator(llm_model)
        self.grid_placer = GridPlacer(llm_model)

    def generate_interior(self, location_description: str) -> list[EnvironmentPart]:
        object_names = self.object_names_generator.generate(location_description)
        objects = self.object_generator.generate(location_description, object_names)
        placed_objects = self.grid_placer.generate(location_description, objects)

        return placed_objects
