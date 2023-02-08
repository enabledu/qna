from uuid import UUID

from fastapi import APIRouter, Depends, Body, Query

from db import get_client
import generated_async_edgeql as queries

answers_router = APIRouter()


# TODO: handle exceptions in the endpoints like NOT FOUND IDs and ViolationConstraintErrors
# FIXME: AsyncIOExecutor or AsyncIOClient
# FIXME: the generated code returns Coroutines?? The problem is in the dataclasses?
# TODO: Handle Auth Stuff

@answers_router.get("/")
async def get_all_answers(client=Depends(get_client)) -> list[queries.GetAllAnswersResult]:
    return queries.get_all_answers(client)


# can Fast API correctly parse the list of IDs from a single path parameter?
@answers_router.get("/answers_subset")
async def get_answers_by_answer_ids(answer_ids: list[UUID] = Query()):
    return queries.get_answers_by_answer_ids(get_client(), ids=answer_ids)


@answers_router.post("/{answer_id}/accept")
async def accept_answer(answer_id: UUID, client=Depends(get_client)):
    return queries.accept_answer(client, id=answer_id)


@answers_router.post("/{answer_id}/accept/undo")
async def undo_accept_answer(answer_id: UUID, client=Depends(get_client)):
    return queries.undo_accept_answer(client, id=answer_id)


@answers_router.get("/{answer_id}/comments")
async def get_comments_on_answer(answer_id: UUID, client=Depends(get_client)):
    return queries.get_comments_on_answer(client, id=answer_id)


@answers_router.post("/{answer_id}/delete")
async def delete_answer(answer_id: UUID, client=Depends(get_client)):
    return delete_answer(client, id=answer_id)


@answers_router.post("/{answer_id}/downvote")
async def downvote_answer(answer_id: UUID, client=Depends(get_client)):
    return queries.downvote_answer(client, id=answer_id)


@answers_router.post("/{answer_id}/downvote/undo")
async def undo_downvote_answer(answer_id: UUID, client=Depends(get_client)):
    return queries.undo_downvote_answer(client, id=answer_id)


@answers_router.post("/{answer_id}/edit")
async def edit_answer(answer_id: UUID, content: str = Body(), client=Depends(get_client)):
    return queries.edit_answer(client, id=answer_id, content=content)


@answers_router.post("/{answer_id}/upvote")
async def upvote_answer(answer_id: UUID, client=Depends(get_client)):
    return queries.upvote_answer(client, id=answer_id)


@answers_router.post("/{answer_id}/upvote/undo")
async def undo_upvote_answer(answer_id: UUID, client=Depends(get_client)):
    return queries.undo_upvote_answer(client, id=answer_id)
