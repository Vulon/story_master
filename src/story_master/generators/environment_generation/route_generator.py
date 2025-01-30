import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.storage.map.map_model import LargeArea, DetailedArea, Route
from story_master.utils.selection import get_batched
from story_master.log import logger

ROUTE_BATCH_SIZE = 3


class RouteIdentifier:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Output all locations that have a direct route between them.
    
    -Steps-
    1. Read the list of locations you need to generate routes between.
        All provided locations are in the same larger area.
    2. Select locations that have a direct route between them.
        You don't need to generate routes between all locations.
    3. For every pair of locations that have a direct route output location IDs. 
    You can output a sentence or two to think, but the main goal is to output the location IDs for routes.
                
    -Locations-
    {locations}        
    
    -Output format-
    Format: (start_location_id, end_location_id), (start_location_id, end_location_id), ...
    
    Output:    
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.route_pattern = re.compile(r"\((\d, \d)\)")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[tuple[int, int]]:
        try:
            output = output.replace("\n", " ")
            raw_routes = self.route_pattern.findall(output)
        except Exception as e:
            logger.error(f"RouteIdentifier. Error parsing output: {output}")
            raise e
        routes = []
        for raw_route in raw_routes:
            try:
                start, end = raw_route.split(", ")
                routes.append((int(start), int(end)))
            except Exception:
                logger.error(f"RouteIdentifier. Error parsing route: {raw_route}")
                continue
        return routes

    def generate(
        self, location_descriptions: str, location_ids: set[int]
    ) -> list[frozenset[int]]:
        raw_routes = self.chain.invoke({"locations": location_descriptions})
        unique_routes = {
            frozenset(route)
            for route in raw_routes
            if int(route[0]) in location_ids and int(route[1]) in location_ids
        }
        return sorted(unique_routes)


class RouteGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Generate all specified routes.
    
    -Steps-
    1. Read the description of locations you need to generate routes between.
        Every location has an ID and a name.
    2. Read the list of routes that you need to generate.
        Every provided route consists of two integers: start and end location IDs.
    3. For every input route generate the following information:
        type: one of the following: land, river, sea, road
        start: id of the starting location
        end: id of the ending location
        distance: float distance in miles
        description: description of the route. Can be very simple like: "A road that goes through the forest.". Can contain information about the terrain.
    4. Output the routes in XML format.
        For every input route output one XML Route block.
      
    -Locations-
    {locations}
    
    -Input routes-
    {input_routes}
    
    -Output example-
    <Route>
        <Type>road</Type>
        <Start>1</Start>
        <End>2</End>
        <Distance>100.0</Distance>
        <Description>A small cobblestone road</Description>
    </Route>
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.route_pattern = re.compile(r"<Route>(.*?)</Route>")
        self.type_pattern = re.compile(r"<Type>(.*?)</Type>")
        self.start_pattern = re.compile(r"<Start>(.*?)</Start>")
        self.end_pattern = re.compile(r"<End>(.*?)</End>")
        self.distance_pattern = re.compile(r"<Distance>(.*?)</Distance>")
        self.description_pattern = re.compile(r"<Description>(.*?)</Description>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

        self.route_identifier = RouteIdentifier(llm_model)

    def parse_output(self, output: str) -> list[Route]:
        try:
            output = output.replace("\n", " ")
            raw_route_strings = self.route_pattern.findall(output)
        except Exception as e:
            logger.error(f"RouteGenerator. Error parsing output: {output}")
            raise e
        routes = []
        for route_string in raw_route_strings:
            try:
                route_type = self.type_pattern.search(route_string).group(1)
                start = self.start_pattern.search(route_string).group(1)
                end = self.end_pattern.search(route_string).group(1)
                distance = self.distance_pattern.search(route_string).group(1)
                description = self.description_pattern.search(route_string).group(1)
                route = Route(
                    type=route_type,
                    start=start,
                    end=end,
                    distance=float(distance),
                    description=description,
                )
                routes.append(route)
            except Exception:
                logger.error(f"RouteGenerator. Error parsing route: {route_string}")
                continue
        return routes

    def generate(
        self,
        locations: list[LargeArea | DetailedArea],
    ) -> list[Route]:
        locations_description = " ; ".join(
            [f"({location.id}: {location.name}.)" for location in locations]
        )
        location_ids = {location.id for location in locations}

        raw_route_ids = self.route_identifier.generate(
            locations_description, location_ids
        )

        raw_route_strings = [f"({start}, {end})" for start, end in raw_route_ids]
        all_output_routes = []
        for routes_batch in get_batched(raw_route_strings, ROUTE_BATCH_SIZE):
            raw_routes = self.chain.invoke(
                {
                    "locations": locations_description,
                    "input_routes": " ; ".join(routes_batch),
                }
            )
            routes = [
                route
                for route in raw_routes
                if route.start in location_ids
                and route.end in location_ids
                and route.start != route.end
            ]
            all_output_routes.extend(routes)
        return all_output_routes
