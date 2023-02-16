import uuid
from http.client import HTTPException
from typing import List, Dict, Optional
import dataclasses
from fastapi import APIRouter, Body
from fastapi import Depends
from edgedb import AsyncIOClient
from fastapi.params import Query


from db import init_db, create_client, close_client, get_client

question_router = APIRouter()

# """"""""" functions """"""


# func to convert from string to list
def str_to_list(string: str) -> list:
    return [tag for tag in string.split(",")]


# func to convert from list of objects  to list dict
def format_query_result(result_list: List) -> List[Dict]:
    return [dataclasses.asdict(element) for element in result_list]


# func of http exception
def http_exception():
    return HTTPException(status_code=404, detail=" ID Not Found ")


# """ get the question by id or title or tags"""
@question_router.get("/")
async def get_by_field_question(
    question_id: Optional[uuid.UUID] = Query(default=None),
    title: Optional[str] = Query(default=None),
    tags: Optional[str] = Query(default=None),
    client: AsyncIOClient = Depends(get_client),
):
    """Get the questions identified by id"""
    #""" define the id of question """
    if question_id:
        question = await client.query_single(
            f"""
             select Question {{
                 id, title, content, upvote, downvote, tags, author
          }} filter .id = <uuid>'{question_id}'
         """
        )
        return dataclasses.asdict(question)
    elif title:
        question = await client.query(
            f"""
             select Question {{
                 id, title, content, upvote, downvote, tags, author
          }} filter .title = <str>'{title}'
         """
        )
        return format_query_result(question)
    else:
        print(
            f"""
             select Question {{
                 id, title, content, upvote, downvote, tags, author
          }} filter .tags = <array<str>>'{tags.split(",")}'
         """
        )
        question = await client.query(
            f"""
             select Question {{
                 id, title, content, upvote, downvote, tags,author
          }} filter .tags = <array<str>>{tags.split(",")}
         """
        )
        return format_query_result(question)


# """ 2) Get the answers to the question identified by id. """
@question_router.get("/{id}/answers")
async def get_answer_by_id(
    question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)
):
    # define the id of asnwers
    question = await client.query_single(
        f"""
                select Question {{
                    answer
                }} filter .id = <uuid>'{question_id}'
            """
    )
    return dataclasses.asdict(question)


# """ 3) Creates an answer on the given question """
@question_router.post("/{id}/answer/add")
async def create_answer(
    question_id: uuid.UUID, content, client: AsyncIOClient = Depends(get_client)
):
    if question_id is None:
        http_exception()
    else:
        answer = await client.query_single(
            f"""
                select (
                     insert Answer {{
                         content := '{content}'
                    }}
                ) {{content}}
            """
        )
        return {"msg": f"creat {answer.id} with content {answer.content} "}


# """ 4) Create a comment on the given question """
@question_router.post("/{id}/comment/add")
async def create_comment(
    question_id: uuid.UUID, content, client: AsyncIOClient = Depends(get_client)
):
    if question_id is None:
        http_exception()
    else:
        comment = await client.query_single(
            f"""
                 select (
                      insert Comment {{
                          content := '{content}',
                     }}
                 ) {{content}}
             """
        )
        return {"msg": f"creat {comment.id} with content {comment.content} "}


# """ 5) Get the comments on the question."""
@question_router.get("/{id}/comments")
async def get_comment_by_id(
    question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)
):
    if not question_id:
        http_exception()
    else:
        question = await client.query_single(
            f"""
                 select Question {{
                     comments
                }} filter .id = <uuid>'{question_id}'
             """
        )
        return format_query_result(question)


# """ 6) Deletes the given questions """
@question_router.delete("/{id}/delete")
async def delete_by_id_question(
    question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)
):
    if not question_id:
        http_exception()
    else:
        await client.query_single(
            f"""
             delete Question  
             filter .id = <uuid>'{question_id}'
         """
        )
        return {"msg": f" Delete Question Successfuly "}


# """ 7) update a downvote on the given question
@question_router.put("/{id}/downvote")
async def update_downvote(
    question_id: uuid.UUID,
    client: AsyncIOClient = Depends(get_client),
):
    if not question_id:
        http_exception()
    else:
        await client.query_single(
            f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{ downvote := .downvote+1}}
         """
        )
        return {"msg": f" update on question downvote Successfuly "}


# """ 8) undo a downvote on the given question
@question_router.put("/{id}/downvote/undo")
async def undo_downvote_question(
    question_id: uuid.UUID,
    client: AsyncIOClient = Depends(get_client),
):
    if not question_id:
        http_exception()
    else:
        await client.query_single(
            f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{ downvote := .downvote-1}}
         """
        )
        return {"msg": f" undo downvote on question Successfuly "}


# """ 9) update a upvote on the given question
@question_router.put("/{id}/upvote")
async def update_upvote(
    question_id: uuid.UUID,
    client: AsyncIOClient = Depends(get_client),
):
    if not question_id:
        http_exception()
    else:
        await client.query_single(
            f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{ upvote := .upvote+1}}
         """
        )
        return {"msg": f" update on question upvote Successfuly "}


# """ 10) undo a upvote on the given question
@question_router.put("/{id}/upvote/undo")
async def undo_upvote_question(
    question_id: uuid.UUID,
    client: AsyncIOClient = Depends(get_client),
):
    if not question_id:
        http_exception()
    else:
        await client.query_single(
            f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{ upvote := .upvote-1}}
         """
        )
        return {"msg": f" undo upvote on question Successfuly "}


# """ 11) Add question
@question_router.post("/add")
async def create_question(
    user_id: uuid.UUID = Body(),
    title: str = Body(),
    content: str = Body(),
    tags: list = Depends(str_to_list),
    client: AsyncIOClient = Depends(get_client),
):
    question = await client.query_single(
        f"""
             select (
                 insert Question {{
                     title := '{title}',
                     content := '{content}',
                     tags := {tags},
                     author := (
                        select User filter .id = <uuid>'{user_id}'
                     )
                 }}
             ) {{id, title, content, tags}}
         """
    )
    return {
        "msg": f"creat {question.id} with date: title {question.title}, and content {question.content}, and tags {question.tags} "
    }


# """ 11) edit question
@question_router.put("/{id}/edit")
async def edit_question(
    question_id: uuid.UUID,
    content=Body(),
    title=Body(),
    client: AsyncIOClient = Depends(get_client),
):
    if not question_id:
        http_exception()
    else:
        await client.query_single(
            f"""
            update Question  
            filter .id = <uuid>'{question_id}'
            set {{  
                content := '{content}' ,
                title := '{title}' ,
                tags := .tags ,
                downvote := .downvote ,
                upvote := .upvote,
                author := .author
                }}
          """
        )
        return {"msg": f"  Edit on question apply Successfuly "}
