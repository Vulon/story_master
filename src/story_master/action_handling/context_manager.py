from typing import Iterable

from story_master.action_handling.parameter import FilledParameter, Parameter
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

    def resolve_providers(self, required_parameters: Iterable[Parameter]) -> None:
        missing_parameters = {
            parameter.name: parameter
            for parameter in required_parameters
            if parameter.name not in self.data
        }
        providers_queue = []
        current_queue_list = []
        while len(missing_parameters) > 0:
            new_missing_parameters = dict()
            for parameter_name, parameter in missing_parameters.items():
                provider = self.table[parameter_name]
                input_parameters = provider.get_input_parameters()
                new_missing_parameters.update(input_parameters)
                current_queue_list.append((provider, parameter))
            missing_parameters = {
                parameter_name: parameter
                for parameter_name, parameter in new_missing_parameters.items()
                if parameter_name not in self.data
            }
            providers_queue.append(current_queue_list)
            current_queue_list = []

        for providers_list in reversed(providers_queue):
            for provider, input_parameter in providers_list:
                filled_input_parameters = {
                    parameter_name: parameter_value.value
                    for parameter_name, parameter_value in self.data.items()
                }
                logger.info(f"Executing provider {provider.get_description()}")
                output_parameters = provider.execute(
                    input_parameter, **filled_input_parameters
                )
                for parameter in output_parameters.values():
                    self.add(parameter)

    def get(self, parameter: Parameter) -> FilledParameter:
        self.resolve_providers([parameter])
        return self.data[parameter.name]
