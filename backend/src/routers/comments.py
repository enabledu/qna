from uuid import UUID

from fastapi import APIRouter, Depends, Body

from enabled.backend.src.database import get_client
from qna.backend.src import queries

comments_router = APIRouter(tags=["qna: comments"], prefix="/comments")


# TODO: handle exceptions in the endpoints like NOT FOUND IDs and ViolationConstraintErrors
# FIXME: AsyncIOExecutor or AsyncIOClient
# TODO: Handle Auth Stuff


@comments_router.get("/")
async def get_all_comments(
    client=Depends(get_client),
):
    response = await queries.get_all_comments(client)
    return response


# @comments_router.get("/answers_commnets")
# async def get_comments_by_ids(
#     comment_ids=Query(), client=Depends(get_client)
# ):
#     response = await queries.get_comments_by_comment_ids(client, ids=comment_ids)
#     return response


@comments_router.post("/{comment_id}/delete")
async def delete_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.delete_comment(client, id=comment_id)
    return response


@comments_router.post("/{comment_id}/downvote")
async def downvote_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.downvote_comment(client, id=comment_id)
    return response


@comments_router.post("/{comment_id}/downvote/undo")
async def undo_downvote_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.undo_downvote_comment(client, id=comment_id)
    return response


@comments_router.post("/{comment_id}/edit")
async def edit_comment(
    comment_id: UUID, content: str = Body(), client=Depends(get_client)
):
    response = await queries.edit_comment(client, id=comment_id, content=content)
    return response


@comments_router.post("/{comment_id}/upvote")
async def upvote_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.upvote_comment(client, id=comment_id)
    return response


@comments_router.post("/{comment_id}/upvote/undo")
async def undo_upvote_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.undo_upvote_comment(client, id=comment_id)
    return response
