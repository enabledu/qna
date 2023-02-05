import uuid
import dataclasses
from fastapi import FastAPI
from fastapi import Depends
from edgedb import AsyncIOClient
from db import init_db, create_client, close_client, get_client

app = FastAPI()


@app.get("/get/{id}")
async def get_by_id(id: uuid.UUID, client: AsyncIOClient = Depends(get_client)):
    question = await client.query_single(f"""
        select Question {{
            id, title, content, upvote, downvote, tags
        }} filter .id = <uuid>'{id}'
    """)

    return dataclasses.asdict(question)


@app.post("/create-q/{title}/{content}")
async def create_question(title, content, client: AsyncIOClient = Depends(get_client)):
    print(f"""
        select (
            insert Question {{
                title := {title},
                content := {content},
            }}
        ) {id, title, content}
    """)

    question = await client.query_single(f"""
        select (
            insert Question {{
                title := '{title}',
                content := '{content}',
                tags := ["A"],
            }}
        ) {{id, title, content}}
    """)

    return {"msg": f"create {question.id} with date: title {question.title}, and content {question.content}"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    await create_client()
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    await close_client()