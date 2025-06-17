from pydantic import BaseModel


class CraftingRequest(BaseModel):
    first_element: str
    second_element: str


class CraftingResponse(BaseModel):
    result: str
    emoji: str
