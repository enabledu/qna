
import uuid
from typing import List, Dict
import dataclasses
from fastapi import FastAPI
from fastapi import Depends, Body
from edgedb import AsyncIOClient
from db import init_db, create_client, close_client, get_client
from answers import answers_router
from questions import question_router

app = FastAPI()
app.include_router(answers_router,
                   prefix="/answers",
                   tags=["answers"])
app.include_router(question_router,
                   prefix="/questions",
                   tags=["questions"])



def str_to_list(string: str) -> list:
    return [tag for tag in string.split(",")]


def format_query_result(result_list: List) -> List[Dict]:
    return [dataclasses.asdict(element) for element in result_list]



@app.on_event("startup")
async def on_startup():
    print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuup")
    await create_client()
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    print("dooooooooooooooooooooooooooooooooooooooooooooooooown")
    await close_client()
