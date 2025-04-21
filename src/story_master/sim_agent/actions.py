from pydantic import BaseModel, Field


class speak_action(BaseModel):
    """
    This action represents character's intent to speak with another character.
    The target character should be nearby.
    """

    speech: str = Field(
        ..., description="The direct speech, that another character will hear"
    )
    another_character_id: int = Field(
        ...,
        description="ID of another character, who is the target for this speak event.",
    )


ANY_ACTION_TYPE = speak_action
ALL_ACTIONS = [speak_action]
