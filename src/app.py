# creat question -- title , cint
# get question
# read (id , title , tags )


import uuid
from typing import List, Dict
import dataclasses
from fastapi import FastAPI
from fastapi import Depends
from edgedb import AsyncIOClient
from db import init_db, create_client, close_client, get_client

app = FastAPI()

def str_to_list(string : str) -> list:
    return [tag for tag in string.split(",")]

def format_query_result(result_list : List) -> List[Dict]:
    return [dataclasses.asdict(element) for element in result_list]

######## create user ##########
@app.post("/creat-q/{title}")
async def create_question(title, content, tags: list = Depends(str_to_list), client: AsyncIOClient = Depends(get_client)):
     question = await client.query_single(f"""
             select (
                 insert Question {{
                     title := '{title}',
                     content := '{content}',
                     tags := {tags}
                 }}
             ) {{id, title, content, tags}}
         """)
     return {"msg": f"creat {question.id} with date: title {question.title}, and content {question.content}, and tags {question.tags} "}

######## create comment ##########
@app.post("/creat-comment")
async def create_comment( content, client: AsyncIOClient = Depends(get_client)):
     comment = await client.query_single(f"""
             select (
                 insert Comment {{
                     content := '{content}',
                 }}
             ) {{content}}
         """)
     return {"msg": f"creat {comment.id} with content {comment.content} "}

######## create answer ##########
@app.post("/creat-answer")
async def create_answer( content, client: AsyncIOClient = Depends(get_client)):
     answer = await client.query_single(f"""
             select (
                 insert Answer {{
                     content := '{content}',
                 }}
             ) {{content}}
         """)
     return {"msg": f"creat {answer.id} with content {answer.content} "}


######## read by id  ##########
@app.get("/get/{id}")
async def get_by_id(id: uuid.UUID, client: AsyncIOClient = Depends(get_client)):
    question = await client.query_single(f"""
         select Question {{
             id, title, content, upvote, downvote, tags
         }} filter .id = <uuid>'{id}'
     """)

    return dataclasses.asdict(question)


######## read by title  ##########
@app.get("/get-title/{title}")
async def get_by_title(title: str, client: AsyncIOClient = Depends(get_client)):
    questions = await client.query(f"""
         select Question {{
             id, title, content, upvote, downvote, tags
         }} filter .title ='{title}' 
     """)

    return format_query_result(questions)


######## read by tags  ##########
@app.get("/get-tags/{tags}")
async def get_by_tags(tags: str, client: AsyncIOClient = Depends(get_client)):
    questions = await client.query(f"""
         select Question {{
             id, title, content, upvote, downvote, tags
         }} filter .tags ='{tags}' 
     """)

    return format_query_result(questions)


######## delete question  ##########
# @app.get("/delete/{id}")
# async def delete_question(id: uuid.UUID, client: AsyncIOClient = Depends(get_client)):
#

@app.on_event("startup")
async def on_startup():
    print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuup")
    await create_client()
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    print("dooooooooooooooooooooooooooooooooooooooooooooooooown")
    await close_client()

