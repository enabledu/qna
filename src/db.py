from typing import AsyncGenerator
from pathlib import Path

import edgedb

client: edgedb.AsyncIOClient


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
    with open(Path("../dbschema/default.esdl")) as f:
        schema = f.read()
    try:
        await client.execute(f"""START MIGRATION TO {{ {schema} }}""")
        await client.execute("""POPULATE MIGRATION""")
        await client.execute("""COMMIT MIGRATION""")
    except:
        pass
