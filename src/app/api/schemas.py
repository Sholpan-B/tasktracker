from uuid import UUID

import pydantic


class TaskSchema(pydantic.BaseModel):
    name: str
    description: str


class TaskGetSchema(pydantic.BaseModel):
    id: UUID | None = pydantic.Field(None)
    name: str | None = pydantic.Field(None)
    description: str | None = pydantic.Field(None, allow_none=True)
    status: str | None = pydantic.Field(None, allow_none=True)


class TaskUpdateSchema(pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    description: str | None = pydantic.Field(None, allow_none=True)
    status: str | None = pydantic.Field(None, allow_none=True)
