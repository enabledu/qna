from typing import AsyncGenerator
from pathlib import Path
from uuid import UUID

from fastapiusers_edgedb import EdgeDBUserDatabase

import edgedb
from pydantic import Field

client: edgedb.AsyncIOClient


class User(EdgeDBUserDatabase):
    id: UUID
    first_name: str
    last_name: str
    username: str
    age: int = Field(ge=0, le=110)
    # posts: list[Post]


async def create_client() -> None:
    global client
    client = edgedb.create_async_client(max_concurrency=3)


async def close_client() -> None:
    await client.aclose()


async def get_client() -> AsyncGenerator[edgedb.AsyncIOClient, None]:
    try:
        yield client
    finally:
        await close_client()


async def init_db():
    with open(Path("dbschema/default.esdl")) as f:
        schema = f.read()
    try:
        await client.execute(f"""START MIGRATION TO {{ {schema} }}""")
        await client.execute("""POPULATE MIGRATION""")
        await client.execute("""COMMIT MIGRATION""")
    except:
        pass


async def get_user_db() -> AsyncGenerator[EdgeDBUserDatabase, None]:
    yield EdgeDBUserDatabase(client)
