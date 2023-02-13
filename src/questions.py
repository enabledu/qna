
import uuid
from http.client import HTTPException
from typing import List, Dict
import dataclasses
from fastapi import FastAPI , Body
from fastapi import Depends
from edgedb import AsyncIOClient

from db import init_db, create_client, close_client, get_client

question = FastAPI()

# """"""""" functions """"""

# """ func to convert from string to list """
def str_to_list(string : str) -> list:
    return [tag for tag in string.split(",")]

 # """ func to convert from list of objects  to list dict """
def format_query_result(result_list : List) -> List[Dict]:
    return [dataclasses.asdict(element) for element in result_list]

def http_exception():
    return HTTPException(status_code=404, detail=" ID Not Found ")

 #""" 1) Get the questions identified by id """
@question.get("/questions/{id}")
async def get_by_id_question(question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)):
    #define the id of question
    question = await client.query_single(f"""
         select Question {{
             id, title, content, upvote, downvote, tags, 
         }} filter .id = <uuid>'{question_id}'
     """)
    return dataclasses.asdict(question)

# """ 2) Get the answers to the question identified by id. """
@question.get("/questions/{id}/answers")
async def get_answer_by_id(question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)):
    #define the id of asnwers
    question = await client.query_single(f"""
                select Question {{
                    answer
                }} filter .id = <uuid>'{question_id}'
            """)
    # return format_query_result(Comment)
    return dataclasses.asdict(question)


# """ 3) Creates an answer on the given question """
@question.post("/questions/{id}/answer/add")
async def create_answer(question_id: uuid.UUID,content, client: AsyncIOClient = Depends(get_client)):
    if question_id is None:
        http_exception()
    else:
         answer = await client.query_single(f"""
                select (
                     insert Answer {{
                         content := '{content}',
                    }}
                ) {{content}}
            """)
         return {"msg": f"creat {answer.id} with content {answer.content} "}


# """ 4) Create a comment on the given question """
@question.post("/questions/{id}/comment/add")
async def create_comment(question_id: uuid.UUID,content, client: AsyncIOClient = Depends(get_client)):
    if question_id is None:
        http_exception()
    else:
        comment = await client.query_single(f"""
                 select (
                      insert Comment {{
                          content := '{content}',
                     }}
                 ) {{content}}
             """)
        return {"msg": f"creat {comment.id} with content {comment.content} "}


# """ 5) Get the comments on the question."""
@question.get("/questions/{id}/comments")
async def get_comment_by_id(question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)):
    if not question_id:
        http_exception()
    else:
        question = await client.query_single(f"""
                 select Question {{
                     comments
                }} filter .id = <uuid>'{question_id}'
             """)
        return format_query_result(question)

# """ 6) Deletes the given questions """
@question.delete("/questions/{id}/delete")
async def delete_by_id_question (question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)):
    if not question_id:
        http_exception()
    else :
        await client.query_single(f"""
             delete Question  
             filter .id = <uuid>'{question_id}'
         """)
        return {"msg": f" Delete Question Successfuly "}

# """ 7) update a downvote on the given question
@question.put("/questions/{id}/downvote")
async def update_downvote(question_id: uuid.UUID,client: AsyncIOClient = Depends(get_client), ):
    if not question_id:
        http_exception()
    else:
        await client.query_single(f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{ downvote := .downvote+1}}
         """)
        return {"msg": f" update on question downvote Successfuly "}


# """ 8) undo a downvote on the given question
@question.put("/questions/{id}/downvote/undo")
async def undo_downvote_question(question_id: uuid.UUID,client: AsyncIOClient = Depends(get_client), ):
    if not question_id:
        http_exception()
    else:
        await client.query_single(f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{ downvote := .downvote-1}}
         """)
        return {"msg": f" undo downvote on question Successfuly "}

# """ 9) update a upvote on the given question
@question.put("/questions/{id}/upvote")
async def update_upvote(question_id: uuid.UUID,client: AsyncIOClient = Depends(get_client), ):
    if not question_id:
        http_exception()
    else:
        await client.query_single(f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{ upvote := .upvote+1}}
         """)
        return {"msg": f" update on question upvote Successfuly "}

# """ 10) undo a upvote on the given question
@question.put("/questions/{id}/upvote/undo")
async def undo_upvote_question(question_id: uuid.UUID,client: AsyncIOClient = Depends(get_client), ):
    if not question_id:
        http_exception()
    else:
        await client.query_single(f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{ upvote := .upvote-1}}
         """)
        return {"msg": f" undo upvote on question Successfuly "}

# """ 11) Add question
@question.post("/questions/add")
async def create_question(title: str = Body(), content: str = Body(), tags: list = Depends(str_to_list), client: AsyncIOClient = Depends(get_client)):
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


# """ 11) edit question
@question.put("/questions/{id}/edit")
async def edit_question(question_id: uuid.UUID,content = Body(),title = Body(),client: AsyncIOClient = Depends(get_client), ):
    if not question_id:
        http_exception()
    else:
        await client.query_single(f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{  
                content := '{content}' ,
                title := '{title}' ,
                tags := .tags ,
                downvote := .downvote ,
                upvote := .upvote
                }}
          """)
        return {"msg": f"  Edit on question apply Successfuly "}


@question.on_event("startup")
async def on_startup():
    print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuup")
    await create_client()
    await init_db()

@question.on_event("shutdown")
async def on_shutdown():
    print("dooooooooooooooooooooooooooooooooooooooooooooooooown")
    await close_client()




