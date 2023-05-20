from uuid import UUID

from qna.backend.src import queries

from qna.backend.src.models import Question, Answer, Comment

from fastapi import HTTPException


async def get_question(question_id: UUID) -> Question:
    question = await queries.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="QUESTION_NOT_FOUND")
    else:
        return question


async def get_answer(answer_id: UUID) -> Answer:
    answer = await queries.get_answer(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="ANSWER_NOT_FOUND")
    else:
        return answer


async def get_comment(comment_id: UUID) -> Comment:
    comment = await queries.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="COMMENT_NOT_FOUND")
    else:
        return comment
