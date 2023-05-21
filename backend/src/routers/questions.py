import dataclasses
from uuid import UUID

from edgedb import AsyncIOClient
from fastapi import APIRouter, Depends, HTTPException

from qna.backend.src import queries

from enabled.backend.src.database import get_client
from enabled.backend.src.users.users import current_active_user

from qna.backend.src.models import (QuestionCreate, QuestionRead, QuestionUpdate,
                                    CommentCreate, CommentRead,
                                    AnswerCreate, AnswerRead,
                                    PostID, ErrorModel)

from qna.backend.src.dependencies import get_question

questions_router = APIRouter(tags=["qna: questions"], prefix="/question")


@questions_router.get("/")
async def get_all_questions(client: AsyncIOClient = Depends(get_client)) -> list[QuestionRead]:
    return await queries.get_all_questions(client)


@questions_router.post("/add/")
async def add_question(question: QuestionCreate,
                       user=Depends(current_active_user),
                       client: AsyncIOClient = Depends(get_client)) -> PostID:
    return await queries.add_question(client, author_id=user.id, **question.dict())


@questions_router.post("/{question_id}/edit/",
                       responses={404: {"model": ErrorModel},
                                  403: {"model": ErrorModel}})
async def edit_question(question_id: UUID,
                        update_question: QuestionUpdate,
                        question: QuestionRead = Depends(get_question),
                        user=Depends(current_active_user),
                        client: AsyncIOClient = Depends(get_client)) -> PostID:
    if not question.author.id == user.id:
        raise HTTPException(status_code=403, detail="ONLY_QUESTION_AUTHOR_CAN_EDIT_IT")
    else:

        question_dict = dataclasses.asdict(question)
        question_dict.update(update_question.dict())
        update_question = {k: v
                           for k, v in question_dict.items()
                           if k in ["title", "content", "tags"]}
        return await queries.edit_question(client, question_id=question_id, **update_question)


@questions_router.delete("/{question_id}/delete/",
                         responses={404: {"model": ErrorModel},
                                    403: {"model": ErrorModel}})
async def delete_question(question_id: UUID,
                          question: QuestionRead = Depends(get_question),
                          user=Depends(current_active_user),
                          client: AsyncIOClient = Depends(get_client)) -> PostID:
    if not question.author.id == user.id:
        raise HTTPException(status_code=403, detail="ONLY_QUESTION_AUTHOR_CAN_DELETE_IT")
    else:
        return await queries.delete_question(client, question_id=question_id)


@questions_router.get("/{question_id}/comment/",
                      dependencies=[Depends(get_question)],
                      responses={404: {"model": ErrorModel}})
async def get_all_question_comments(question_id: UUID,
                                    client: AsyncIOClient = Depends(get_client)) -> list[CommentRead]:
    return await queries.get_all_question_comments(client, question_id=question_id)


@questions_router.post("/{question_id}/comment/add/",
                       dependencies=[Depends(get_question)],
                       responses={404: {"model": ErrorModel}})
async def add_comment_to_question(question_id: UUID,
                                  comment: CommentCreate,
                                  user=Depends(current_active_user),
                                  client: AsyncIOClient = Depends(get_client)) -> PostID:
    return await queries.add_comment_to_question(client,
                                                 author_id=user.id,
                                                 content=comment.content,
                                                 question_id=question_id)


@questions_router.get("/{question_id}/answer/",
                      dependencies=[Depends(get_question)],
                      responses={404: {"model": ErrorModel}})
async def get_all_question_answers(question_id: UUID,
                                   client: AsyncIOClient = Depends(get_client)) -> list[AnswerRead]:
    return await queries.get_all_question_answers(client, question_id=question_id)


@questions_router.post("/{question_id}/answer/add/",
                       dependencies=[Depends(get_question)],
                       responses={404: {"model": ErrorModel}})
async def add_answer_to_question(question_id: UUID,
                                 answer: AnswerCreate,
                                 user=Depends(current_active_user),
                                 client: AsyncIOClient = Depends(get_client)) -> PostID:
    return await queries.add_answer_to_question(client,
                                                author_id=user.id,
                                                content=answer.content,
                                                question_id=question_id)


@questions_router.post("/{question_id}/upvote/",
                       dependencies=[Depends(get_question)],
                       responses={404: {"model": ErrorModel}})
async def upvote_question(question_id: UUID,
                          user=Depends(current_active_user),
                          client: AsyncIOClient = Depends(get_client)) -> PostID:
    return await queries.upvote_post(client,
                                     post_id=question_id,
                                     upvoter_id=user.id)


@questions_router.post("/{question_id}/upvote/undo/",
                       dependencies=[Depends(get_question)],
                       responses={404: {"model": ErrorModel}})
async def undo_upvote_question(question_id: UUID,
                               user=Depends(current_active_user),
                               client: AsyncIOClient = Depends(get_client)) -> PostID:
    return await queries.undo_upvote_post(client,
                                          post_id=question_id,
                                          upvoter_id=user.id)


@questions_router.post("/{question_id}/downvote/",
                       dependencies=[Depends(get_question)],
                       responses={404: {"model": ErrorModel}})
async def downvote_question(question_id: UUID,
                            user=Depends(current_active_user),
                            client: AsyncIOClient = Depends(get_client)) -> PostID:
    return await queries.downvote_post(client,
                                       post_id=question_id,
                                       downvoter_id=user.id)


@questions_router.post("/{question_id}/downvote/undo/",
                       dependencies=[Depends(get_question)],
                       responses={404: {"model": ErrorModel}})
async def undo_downvote_question(question_id: UUID,
                                 user=Depends(current_active_user),
                                 client: AsyncIOClient = Depends(get_client)) -> PostID:
    return await queries.undo_downvote_post(client,
                                            post_id=question_id,
                                            downvoter_id=user.id)
