from pydantic import BaseModel


class Parameter(BaseModel):
    name: str
    description: str
    required: bool = True


class FilledParameter(Parameter):
    value: object
