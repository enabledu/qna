import dataclasses
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from enabled.backend.src.database import get_client

from qna.backend.src import queries

from qna.backend.src.models import (AnswerCreate, AnswerRead, AnswerUpdate,
                                    CommentCreate, CommentRead,
                                    PostID, ErrorModel)

from enabled.backend.src.users.users import current_active_user

from qna.backend.src.dependencies import get_answer

answers_router = APIRouter(tags=["qna: answers"], prefix="/answer")


@answers_router.post("/{answer_id}/edit/",
                     responses={404: {"model": ErrorModel},
                                403: {"model": ErrorModel}})
async def edit_answer(answer_id: UUID,
                      update_answer: AnswerUpdate,
                      answer: AnswerRead = Depends(get_answer),
                      user=Depends(current_active_user),
                      client=Depends(get_client)) -> PostID:
    if not answer.author.id == user.id:
        raise HTTPException(status_code=403, detail="ONLY_ANSWER_AUTHOR_CAN_EDIT_IT")
    else:
        answer_dict = dataclasses.asdict(answer)
        answer_dict.update(update_answer.dict())
        update_answer = {k: v
                         for k, v in answer_dict.items()
                         if k in ['content']}
        return await queries.edit_answer(client, answer_id=answer_id, **update_answer)


@answers_router.post("/{answer_id}/delete/",
                     responses={404: {"model": ErrorModel},
                                403: {"model": ErrorModel}})
async def delete_answer(answer_id: UUID,
                        answer: AnswerRead = Depends(get_answer),
                        user=Depends(current_active_user),
                        client=Depends(get_client)) -> PostID:
    if not answer.author.id == user.id:
        raise HTTPException(status_code=403, detail="ONLY_ANSWER_AUTHOR_CAN_DELETE_IT")
    else:
        return await queries.delete_answer(client, answer_id=answer_id)


@answers_router.get("/{answer_id}/comment/",
                    dependencies=[Depends(get_answer)],
                    responses={404: {"model": ErrorModel}})
async def get_all_answer_comments(answer_id: UUID,
                                  client=Depends(get_client)) -> list[CommentRead]:
    return await queries.get_all_answer_comments(client, answer_id=answer_id)


@answers_router.post("/{answer_id}/comment/add/",
                     dependencies=[Depends(get_answer)],
                     responses={404: {"model": ErrorModel}})
async def add_comment_to_answer(answer_id: UUID,
                                comment: CommentCreate,
                                user=Depends(current_active_user),
                                client=Depends(get_client)) -> PostID:
    return await queries.add_comment_to_answer(client,
                                               author_id=user.id,
                                               content=comment.content,
                                               answer_id=answer_id)


@answers_router.post("/{answer_id}/accept/",
                     responses={404: {"model": ErrorModel}})
async def accept_answer(answer_id: UUID,
                        answer: AnswerRead = Depends(get_answer),
                        user=Depends(current_active_user),
                        client=Depends(get_client)) -> PostID:
    if not answer.author.id == user.id:
        raise HTTPException(status_code=403, detail="ONLY_ANSWER_AUTHOR_CAN_ACCEPT_IT")
    else:
        return await queries.accept_answer(client, answer_id=answer_id)


@answers_router.post("/{answer_id}/accept/undo/",
                     responses={404: {"model": ErrorModel}})
async def undo_accept_answer(answer_id: UUID,
                             answer: AnswerRead = Depends(get_answer),
                             user=Depends(current_active_user),
                             client=Depends(get_client)) -> PostID:
    if not answer.author.id == user.id:
        raise HTTPException(status_code=403, detail="ONLY_ANSWER_AUTHOR_CAN_UNDO_ACCEPT_IT")
    else:
        return await queries.undo_accept_answer(client, answer_id=answer_id)


@answers_router.post("/{answer_id}/upvote/",
                     dependencies=[Depends(get_answer)],
                     responses={404: {"model": ErrorModel}})
async def upvote_answer(answer_id: UUID,
                        user=Depends(current_active_user),
                        client=Depends(get_client)) -> PostID:
    return await queries.upvote_post(client,
                                     post_id=answer_id,
                                     upvoter_id=user.id)


@answers_router.post("/{answer_id}/upvote/undo/",
                     dependencies=[Depends(get_answer)],
                     responses={404: {"model": ErrorModel}})
async def undo_upvote_answer(answer_id: UUID,
                             user=Depends(current_active_user),
                             client=Depends(get_client)) -> PostID:
    return await queries.undo_upvote_post(client,
                                          post_id=answer_id,
                                          upvoter_id=user.id)


@answers_router.post("/{answer_id}/downvote/",
                     dependencies=[Depends(get_answer)],
                     responses={404: {"model": ErrorModel}})
async def downvote_answer(answer_id: UUID,
                          user=Depends(current_active_user),
                          client=Depends(get_client)) -> PostID:
    return await queries.downvote_post(client,
                                       post_id=answer_id,
                                       downvoter_id=user.id)


@answers_router.post("/{answer_id}/downvote/undo/",
                     dependencies=[Depends(get_answer)],
                     responses={404: {"model": ErrorModel}})
async def undo_downvote_answer(answer_id: UUID,
                               user=Depends(current_active_user),
                               client=Depends(get_client)) -> PostID:
    return await queries.undo_downvote_post(client,
                                            post_id=answer_id,
                                            downvoter_id=user.id)
