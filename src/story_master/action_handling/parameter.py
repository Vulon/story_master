from pydantic import BaseModel


class Parameter(BaseModel):
    name: str
    description: str


class FilledParameter(Parameter):
    value: object
