import time

from langchain_core.language_models.chat_models import BaseChatModel
from story_master.log import logger
from story_master.entities.location import Region, Position
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.generators.environment_generation.decomposer import MapDecomposer
from story_master.generators.environment_generation.object_generator import (
    ObjectNameGenerator,
    ObjectGenerator,
    ObjectPlacer,
    DEFAULT_GENERATION_RADIUS,
)

THRESHOLD_OBJECTS_COUNT = (DEFAULT_GENERATION_RADIUS**2) * 0.4
MAP_GENERATION_STRIDE = 3


class MapCreator:
    def __init__(
        self,
        llm_model: BaseChatModel,
        storage_handler: StorageHandler,
        summary_handler: SummaryHandler,
    ):
        self.llm_model = llm_model
        self.storage_manager = storage_handler
        self.summary_handler = summary_handler

        self.map_decomposer = MapDecomposer(llm_model)

        self.object_name_generator = ObjectNameGenerator(llm_model)
        self.object_generator = ObjectGenerator(llm_model)
        self.object_placer = ObjectPlacer(llm_model)

    def generate_patch(self, center: Position) -> None:
        start = time.time()
        min_x = center.x - DEFAULT_GENERATION_RADIUS / 2
        max_x = center.x + DEFAULT_GENERATION_RADIUS / 2
        min_y = center.y - DEFAULT_GENERATION_RADIUS / 2
        max_y = center.y + DEFAULT_GENERATION_RADIUS / 2
        region: Region = self.storage_manager.get_location(center.location_id)
        if not isinstance(region, Region):
            logger.error(f"Can only generate objects in regions, got {region}")
            return
        objects = filter(
            lambda obj: min_x <= obj.position.x <= max_x, region.objects.values()
        )
        objects = filter(lambda obj: min_y <= obj.position.y <= max_y, objects)
        shifted_objects = []
        existing_positions = set()
        for obj in objects:
            obj.position.x -= center.x
            obj.position.y -= center.y
            existing_positions.add((obj.position.x, obj.position.y))
            shifted_objects.append(obj)
        if len(shifted_objects) >= THRESHOLD_OBJECTS_COUNT:
            logger.info(f"Skipping generation for region {region.id}, too many objects")
            return
        logger.info(f"Region objects: {len(region.objects)}")
        logger.info(f"Objects in range: {len(shifted_objects)}")

        new_object_names = self.object_name_generator.generate(region, shifted_objects)
        logger.info(f"New generated names: {new_object_names}")
        raw_objects = self.object_generator.generate(region, new_object_names)
        for i, raw_object in enumerate(raw_objects):
            raw_object.id = i
        placed_objects = self.object_placer.generate(
            region, shifted_objects, raw_objects
        )
        final_new_objects = []
        new_object_id = max(region.objects.keys()) + 1 if region.objects else 0
        for obj in placed_objects:
            if (obj.position.x, obj.position.y) in existing_positions:
                continue
            obj.position.x += center.x
            obj.position.y += center.y
            obj.id = new_object_id
            new_object_id += 1
            final_new_objects.append(obj)
            logger.info(
                f"Placed object {obj.name} at {obj.position.x}, {obj.position.y}"
            )
            region.objects[obj.id] = obj
        logger.info(
            f"Generated {len(final_new_objects)} objects in {time.time() - start:.2f} seconds"
        )

    def generate_area(self, center: Position, radius: int):
        """
        Move in a circle around the center and generate objects.
        Start from the top left corner and move clockwise.
        Increase the radius by stride with every full iteration.

        """
        generation_coordinates = []
        # Calculate total count of iterations based on radius, stride and default generation radius for a patch
        space = radius - DEFAULT_GENERATION_RADIUS
        logger.info(f"Generating area with radius {radius}. Space: {space}")
        iterations = max(0, space // MAP_GENERATION_STRIDE) + 1
        logger.info(f"Iterations: {iterations}")
        for i in range(1, iterations + 1):
            offset = i * MAP_GENERATION_STRIDE
            single_side_iterations = i * 2
            x = center.x - offset
            y = center.y - offset
            logger.info(
                f"Iteration {i}. Offset {offset}. Single side iterations {single_side_iterations}. X: {x}, Y: {y}"
            )
            for _ in range(single_side_iterations):
                generation_coordinates.append((x, y))
                y += MAP_GENERATION_STRIDE
            for _ in range(single_side_iterations):
                generation_coordinates.append((x, y))
                x += MAP_GENERATION_STRIDE
            for _ in range(single_side_iterations):
                generation_coordinates.append((x, y))
                y -= MAP_GENERATION_STRIDE
            for _ in range(single_side_iterations):
                generation_coordinates.append((x, y))
                x -= MAP_GENERATION_STRIDE
        logger.info(f"Coordinates: {generation_coordinates}")
        for x, y in generation_coordinates:
            position = Position(x=x, y=y, location_id=center.location_id)
            self.generate_patch(position)

    def create_map(self) -> None:
        logger.info("Creating map")
        raw_regions = self.map_decomposer.generate()
        for raw_region in raw_regions:
            region_id = 0
            if location_ids := self.storage_manager.map.locations.keys():
                region_id = max(location_ids) + 1
            position = Position(x=raw_region.x, y=raw_region.y, location_id=None)
            region = Region(
                id=region_id,
                name=raw_region.name,
                description=raw_region.description,
                position=position,
            )
            self.storage_manager.map.locations[region_id] = region

        logger.info("Generating patch")
        starting_region = self.storage_manager.map.locations[0]
        center_position = Position(x=0, y=0, location_id=starting_region.id)
        self.generate_patch(center_position)

        self.storage_manager.save_map()
