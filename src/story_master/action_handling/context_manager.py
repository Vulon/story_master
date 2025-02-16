from typing import Iterable

from story_master.action_handling.parameter import FilledParameter
from story_master.action_handling.providers.provider import Provider
from story_master.log import logger


class ContextManager:
    def __init__(self, providers: list[Provider]):
        self.data = {}
        self.providers = providers
        self.table: dict[str, Provider] = {
            parameter_name: provider
            for provider in providers
            for parameter_name in provider.get_output_parameters().keys()
        }

    def clear(self):
        self.data = {}

    def add(self, parameter: FilledParameter) -> None:
        self.data[parameter.name] = parameter

    def is_parameter_filled(self, parameter_name: str) -> bool:
        return parameter_name in self.data

    def resolve_providers(self, parameter_names: Iterable[str]) -> None:
        missing_parameters = set(parameter_names) - set(self.data.keys())
        providers_queue = []
        current_queue_list = []
        while len(missing_parameters) > 0:
            new_missing_parameters = set()
            for parameter_name in missing_parameters:
                provider = self.table[parameter_name]
                input_parameters = provider.get_input_parameters()
                new_missing_parameters.update(
                    set(input_parameters.keys()) - set(self.data.keys())
                )
                current_queue_list.append(provider)
            missing_parameters = new_missing_parameters
            providers_queue.append(current_queue_list)
            current_queue_list = []

        for providers_list in reversed(providers_queue):
            for provider in providers_list:
                filled_input_parameters = {
                    parameter_name: parameter_value.value
                    for parameter_name, parameter_value in self.data.items()
                }
                logger.info(f"Executing provider {provider.get_description()}")
                output_parameters = provider.execute(**filled_input_parameters)
                for parameter in output_parameters.values():
                    self.add(parameter)

    def get(self, parameter_name: str) -> FilledParameter:
        self.resolve_providers([parameter_name])
        return self.data[parameter_name]
