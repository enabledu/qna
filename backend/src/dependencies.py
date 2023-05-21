from uuid import UUID

from edgedb import AsyncIOClient
from qna.backend.src import queries

from qna.backend.src.models import QuestionRead, AnswerRead, CommentRead

from fastapi import HTTPException, Depends

from enabled.backend.src.database import get_client


async def get_question(question_id: UUID,
                       client: AsyncIOClient = Depends(get_client)) -> QuestionRead:
    question = await queries.get_question(client, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="QUESTION_NOT_FOUND")
    else:
        return question


async def get_answer(answer_id: UUID,
                     client: AsyncIOClient = Depends(get_client)) -> AnswerRead:
    answer = await queries.get_answer(client, answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="ANSWER_NOT_FOUND")
    else:
        return answer


async def get_comment(comment_id: UUID,
                      client: AsyncIOClient = Depends(get_client)) -> CommentRead:
    comment = await queries.get_comment(client, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="COMMENT_NOT_FOUND")
    else:
        return comment
