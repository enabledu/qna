import uuid
from typing import Optional

from edgedb import AsyncIOClient
from fastapi import APIRouter, Body, Depends, Query

from enabled.backend.src.database import get_client
from qna_app.backend.src.utils import format_query_result, str_to_list

question_router = APIRouter(prefix="/question")


@question_router.get("/")
async def get_q_by_field(field, value, client: AsyncIOClient = Depends(get_client)):
    """Get the questions identified by id or title"""
    cast_dict = {"title": "<str>", "id": "<uuid>"}
    filter_expression = f"""filter .{field} = {cast_dict[field]}'{value}'"""
    query_expression = f"""
        select Question {{
                 id, title, content, upvote, downvote, tags, author
          }} {filter_expression}
    """
    return await client.query(query_expression)


@question_router.get("/{id}/answers")
async def get_answers(
    question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)
):
    """Get the answers of the question identified by id"""
    answers = await client.query(
        f"""
        select Question {{
            answer
        }} filter .id = <uuid>'{question_id}'
    """
    )
    return format_query_result(answers)


async def get_insert_query(
    question_id: uuid.UUID,
    author_id: uuid.UUID,
    child_type: str,
    content,
):
    """Get the query to insert a comment or answer"""
    child_fields = {"Comment": "comments", "Answer": "answer"}
    insert_query = f"""
                with
                child := (
                    insert {child_type} {{
                        content := '{content}',
                        author := (select User filter .id = <uuid>'{author_id}')
                    }}
                ),
                question := (
                    update Question filter .id = <uuid>'{question_id}'
                        set {{
                            {child_fields[child_type]} += child
                        }}
                    )
                select (child, question)
            """
    return insert_query


@question_router.post("/{id}/answer/add")
async def insert_answer(
    question_id: uuid.UUID,
    author_id: uuid.UUID,
    content,
    client: AsyncIOClient = Depends(get_client),
):
    """Insert an answer to the question"""
    insert_query = await get_insert_query(question_id, author_id, "Answer", content)
    return await client.query(insert_query)


@question_router.post("/{id}/comment/add")
async def insert_comment(
    question_id: uuid.UUID,
    author_id: uuid.UUID,
    content,
    client: AsyncIOClient = Depends(get_client),
):
    """Insert a comment to the question"""
    insert_query = await get_insert_query(question_id, author_id, "Comment", content)
    return await client.query(insert_query)


@question_router.get("/{id}/comments")
async def get_q_comments(
    question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)
):
    """Get the comments of the question identified by id"""
    question = await client.query_single(
        f"""
        select Question {{
            comments
        }} filter .id = <uuid>'{question_id}'
    """
    )
    return format_query_result(question)


@question_router.delete("/{id}/delete")
async def delete_by_id_question(
    question_id: uuid.UUID, client: AsyncIOClient = Depends(get_client)
):
    """Delete the question identified by id"""
    deleted_question = await client.query_single(
        f"""delete Question filter .id = <uuid>'{question_id}'"""
    )
    return {"msg": f" Delete Question {deleted_question.id} Successfully "}


async def get_vote_query(questio_id: uuid.UUID, vote_type: str, value: int):
    operator = "+" if value > 0 else "-"
    query_expression = f"""
        update Question  
        filter .id = <uuid>'{questio_id}'
        set {{ {vote_type} := .{vote_type}{operator}{value}}}
     """
    return query_expression


@question_router.put("/{id}/upvote")
async def upvote(
    question_id: uuid.UUID,
    client: AsyncIOClient = Depends(get_client),
):
    """Upvote on the question identified by id"""
    upvote_query = await get_vote_query(question_id, "upvote", 1)
    return await client.query_single(upvote_query)


@question_router.put("/{id}/downvote")
async def downvote(
    question_id: uuid.UUID,
    client: AsyncIOClient = Depends(get_client),
):
    """Downvote on the question identified by id"""
    downvote_query = await get_vote_query(question_id, "downvote", 1)
    return await client.query_single(downvote_query)


@question_router.put("/{id}/downvote/undo")
async def undo_downvote(
    question_id: uuid.UUID,
    client: AsyncIOClient = Depends(get_client),
):
    """Undo downvote on the question identified by id"""
    undo_downvote_query = await get_vote_query(question_id, "downvote", -1)
    return await client.query_single(undo_downvote_query)


@question_router.put("/{id}/upvote/undo")
async def undo_upvote(
    question_id: uuid.UUID,
    client: AsyncIOClient = Depends(get_client),
):
    undo_upvote_query = await get_vote_query(question_id, "upvote", -1)
    return await client.query_single(undo_upvote_query)


@question_router.post("/add")
async def create_question(
    user_id: uuid.UUID = Body(),
    title: str = Body(),
    content: str = Body(),
    tags: list = Depends(str_to_list),
    client: AsyncIOClient = Depends(get_client),
):
    """Create a new question"""
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
    return {"msg": f"create {question.id}"}


@question_router.put("/{id}/edit")
async def edit_question(
    question_id: uuid.UUID,
    content: Optional[str] = Query(default=".content"),
    title: Optional[str] = Query(default=".title"),
    client: AsyncIOClient = Depends(get_client),
):
    update_question_query = f"""
        select (
            update Question filter .id = <uuid>'{question_id}'
            set {{
                content := '{content}',
                title := '{title}',
                tags := .tags,
                downvote := .downvote,
                upvote := .upvote,
                author := .author
            }}) {{id}}
    """
    updated_question = await client.query_single(update_question_query)
    return {"msg": f"  Edit on question {updated_question.id} apply Successfully "}
