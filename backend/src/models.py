from uuid import UUID

from pydantic import BaseModel, Field


class ErrorModel(BaseModel):
    detail: str


class Author(BaseModel):
    id: UUID
    username: str


class PostID(BaseModel):
    id: UUID


class PostVote(BaseModel):
    id: UUID
    upvotes: int = Field(ge=0)
    downvotes: int  = Field(ge=0)


class QuestionRead(BaseModel):
    id: UUID
    content: str
    upvotes: int = 0
    downvotes: int = 0
    author: Author
    title: str
    tags: list[str] = None


class QuestionUpdate(BaseModel):
    content: str
    title: str
    tags: list[str] = None


class QuestionCreate(BaseModel):
    content: str
    title: str
    tags: list[str] = None


class AnswerRead(BaseModel):
    id: UUID
    content: str
    upvotes: int = 0
    downvotes: int = 0
    author: Author
    is_accepted: bool = False


class AnswerCreate(BaseModel):
    content: str


class AnswerUpdate(BaseModel):
    content: str


class CommentRead(BaseModel):
    id: UUID
    content: str
    upvotes: int = 0
    downvotes: int = 0
    author: Author


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str
