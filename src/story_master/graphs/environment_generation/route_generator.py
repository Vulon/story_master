import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.storage.map.map_model import Location, Route

# TODO: Optimize generation. Present only 3-4 locations at a time. Generate routes between them.


class RouteGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Generate all routes between specified locations.
    
    -Steps-
    1. Read the list of locations you need to generate routes between.
        All provided locations are in the same larger area.
    2. Select locations that have a direct route between them.
        You don't need to generate routes between all locations.
    3. For every route output all fields:
        type: one of the following: land, river, sea, road
        start: id of the starting location
        end: id of the ending location
        distance: float distance in miles
        description: description of the route. Can be very simple like: "A road that goes through the forest.". Can contain information about the terrain.
    4. Output the routes in XML format.
    <Route>
        <Type>road</Type>
        <Start>1</Start>
        <End>2</End>
        <Distance>100.0</Distance>
        <Description>A small cobblestone road</Description>
    </Route>
    
    -General area-
    {general_area}
    
    -Locations-
    {locations}
    
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.route_pattern = re.compile(r"<Route>(.*?)</Route>")
        self.type_pattern = re.compile(r"<Type>(.*)</Type>")
        self.start_pattern = re.compile(r"<Start>(.*)</Start>")
        self.end_pattern = re.compile(r"<End>(.*)</End>")
        self.distance_pattern = re.compile(r"<Distance>(.*)</Distance>")
        self.description_pattern = re.compile(r"<Description>(.*)</Description>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[Route]:
        output = output.replace("\n", " ")
        raw_route_strings = self.route_pattern.findall(output)
        routes = []
        for route_string in raw_route_strings:
            print("New route")
            print(route_string)
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
        return routes

    def generate(
        self, locations: list[Location], parent_location: Location
    ) -> list[Route]:
        locations_description = " ; ".join(
            [
                f"({location.id}: {location.name}. {location.short_description})"
                for location in locations
            ]
        )
        location_ids = {location.id for location in locations}
        general_area = f"{parent_location.name}: {parent_location.short_description}"
        raw_routes = self.chain.invoke(
            {"locations": locations_description, "general_area": general_area}
        )
        routes = [
            route
            for route in raw_routes
            if route.start in location_ids
            and route.end in location_ids
            and route.start != route.end
        ]
        return routes
