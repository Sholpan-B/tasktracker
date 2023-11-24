from uuid import UUID

import pydantic


class TaskSchema(pydantic.BaseModel):
    name: str
    description: str


class TaskGetSchema(TaskSchema):
    id: UUID | None
    name: str | None
    description = str | None
