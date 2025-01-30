from story_master.action_handling.parameter import Parameter

from story_master.action_handling.providers.provider import Provider
from story_master.action_handling.parameter import FilledParameter


class LocationProvider(Provider):
    def get_description(self) -> str:
        return "Find the location for the action"

    def get_input_parameters(self) -> dict[str, Parameter]:
        return {
            "intent": Parameter(
                name="intent",
                description="The intent for the action",
            )
        }

    def get_output_parameters(self) -> dict[str, Parameter]:
        return {
            "location_id": Parameter(
                name="location_id",
                description="The location where the action should be performed",
            )
        }

    def execute(
        self, intent: str, actor_character_id: int | None = None, **kwargs
    ) -> dict[str, FilledParameter]:
        if actor_character_id is None:
            raise NotImplementedError(
                "Location search without character id is not implemented yet"
            )
        else:
            sim = self.storage_manager.get_sim(actor_character_id)
            location_id = sim.current_location_id
            return {
                "location_id": FilledParameter(
                    name="location_id",
                    value=location_id,
                    description="The location where the action should be performed",
                )
            }
