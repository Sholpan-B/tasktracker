from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "surname" VARCHAR(100) NOT NULL,
    "email" VARCHAR(200) NOT NULL UNIQUE,
    "password" VARCHAR(300) NOT NULL,
    "date_registered" DATE NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user";"""
