from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tag" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL
);
        CREATE TABLE IF NOT EXISTS "tag_task" (
    "task_id" UUID NOT NULL REFERENCES "task" ("id") ON DELETE CASCADE,
    "tag_id" UUID NOT NULL REFERENCES "tag" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "tag_task";
        DROP TABLE IF EXISTS "tag";"""
