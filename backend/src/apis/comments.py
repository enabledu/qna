from uuid import UUID

from fastapi import APIRouter, Depends, Body, Query

from core.backend.src.database import get_client
from qna_app.backend.src.apis import generated_async_edgeql as queries

answers_router = APIRouter()


# TODO: handle exceptions in the endpoints like NOT FOUND IDs and ViolationConstraintErrors
# FIXME: AsyncIOExecutor or AsyncIOClient
# TODO: Handle Auth Stuff

@answers_router.get("/")
async def get_all_comments(client=Depends(get_client)) -> list[queries.GetAllCommentsResult]:
    response = await queries.get_all_comments(client)
    return response

@answers_router.get("/answers_subset")
async def get_comments_by_comment_ids(comment_ids: list[UUID] = Query(), client=Depends(get_client)):
    response = await queries.get_comments_by_comment_ids(client, ids=comment_ids)
    return response

@answers_router.post("/{comment_id}/delete")
async def delete_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.delete_comment(client, id=comment_id)
    return response

@answers_router.post("/{comment_id}/downvote")
async def downvote_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.downvote_comment(client, id=comment_id)
    return response

@answers_router.post("/{comment_id}/downvote/undo")
async def undo_downvote_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.undo_downvote_comment(client, id=comment_id)
    return response

@answers_router.post("/{comment_id}/edit")
async def edit_comment(comment_id: UUID, content: str = Body(), client=Depends(get_client)):
    response = await queries.edit_comment(client, id=comment_id, content=content)
    return response

@answers_router.post("/{comment_id}/upvote")
async def upvote_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.upvote_comment(client, id=comment_id)
    return response

@answers_router.post("/{comment_id}/upvote/undo")
async def undo_upvote_comment(comment_id: UUID, client=Depends(get_client)):
    response = await queries.undo_upvote_comment(client, id=comment_id)
    return response
