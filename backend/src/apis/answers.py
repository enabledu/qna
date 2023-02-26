from uuid import UUID

from fastapi import APIRouter, Depends, Body, Query

from enabled.backend.src.database import get_client

from qna_app.backend.src.apis import generated_async_edgeql as queries

answers_router = APIRouter()


# TODO: handle exceptions in the endpoints like NOT FOUND IDs and ViolationConstraintErrors
# FIXME: AsyncIOExecutor or AsyncIOClient
# TODO: Handle Auth Stuff

@answers_router.get("/")
async def get_all_answers(client=Depends(get_client)) -> list[queries.GetAllAnswersResult]:
    response = await queries.get_all_answers(client)
    return response


@answers_router.get("/answers_subset")
async def get_answers_by_answer_ids(answer_ids: list[UUID] = Query(), client=Depends(get_client)):
    response = await queries.get_answers_by_answer_ids(client, ids=answer_ids)
    return response


@answers_router.post("/{answer_id}/accept")
async def accept_answer(answer_id: UUID, client=Depends(get_client)):
    response = await queries.accept_answer(client, id=answer_id)
    return response


@answers_router.post("/{answer_id}/accept/undo")
async def undo_accept_answer(answer_id: UUID, client=Depends(get_client)):
    response = await queries.undo_accept_answer(client, id=answer_id)
    return response


@answers_router.get("/{answer_id}/comments")
async def get_comments_on_answer(answer_id: UUID, client=Depends(get_client)):
    response = await queries.get_comments_on_answer(client, id=answer_id)
    return response


@answers_router.post("/{answer_id}/delete")
async def delete_answer(answer_id: UUID, client=Depends(get_client)):
    response = await delete_answer(client, id=answer_id)
    return response


@answers_router.post("/{answer_id}/downvote")
async def downvote_answer(answer_id: UUID, client=Depends(get_client)):
    response = await queries.downvote_answer(client, id=answer_id)
    return response


@answers_router.post("/{answer_id}/downvote/undo")
async def undo_downvote_answer(answer_id: UUID, client=Depends(get_client)):
    response = await queries.undo_downvote_answer(client, id=answer_id)
    return response


@answers_router.post("/{answer_id}/edit")
async def edit_answer(answer_id: UUID, content: str = Body(), client=Depends(get_client)):
    response = await queries.edit_answer(client, id=answer_id, content=content)
    return response


@answers_router.post("/{answer_id}/upvote")
async def upvote_answer(answer_id: UUID, client=Depends(get_client)):
    response = await queries.upvote_answer(client, id=answer_id)
    return response


@answers_router.post("/{answer_id}/upvote/undo")
async def undo_upvote_answer(answer_id: UUID, client=Depends(get_client)):
    response = await queries.undo_upvote_answer(client, id=answer_id)
    return response





