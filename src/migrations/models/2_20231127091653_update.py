from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ADD "author_id" UUID NOT NULL;
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL
);
        ALTER TABLE "task" ADD CONSTRAINT "fk_task_user_2cb5ede0" FOREIGN KEY ("author_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" DROP CONSTRAINT "fk_task_user_2cb5ede0";
        ALTER TABLE "task" DROP COLUMN "author_id";
        ALTER TABLE "task" DROP COLUMN "status";
        DROP TABLE IF EXISTS "user";"""
