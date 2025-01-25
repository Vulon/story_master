from story_master.action_handling.parameter import FilledParameter
from story_master.action_handling.providers.provider import Provider


class ContextManager:
    def __init__(self, providers: list[Provider]):
        self.data = {}
        self.providers = providers
        self.table = {
            parameter_name: provider
            for provider in providers
            for parameter_name in provider.get_output_parameters().keys()
        }

    def add(self, parameter: FilledParameter) -> None:
        self.data[parameter.name] = parameter
