from pydantic import BaseModel


class RagExampleEventSchema(BaseModel):
    query: str
