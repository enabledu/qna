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


class QuestionCreate(BaseModel):
    content: str
    title: str
    tags: list[str] = None


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


class AnswerRead(BaseModel):
    id: UUID
    content: str
    upvotes: int = 0
    downvotes: int = 0
    author: Author
    is_accepted: bool = False


class AnswerReadDetailed(BaseModel):
    id: UUID
    content: str
    upvotes: int = 0
    downvotes: int = 0
    author: Author
    is_accepted: bool = False

    comments: list[CommentRead] = None


class AnswerCreate(BaseModel):
    content: str


class AnswerUpdate(BaseModel):
    content: str


class QuestionRead(BaseModel):
    id: UUID
    content: str
    upvotes: int = 0
    downvotes: int = 0
    author: Author
    title: str
    tags: list[str] = None


class QuestionReadDetailed(BaseModel):
    id: UUID
    content: str
    upvotes: int = 0
    downvotes: int = 0
    author: Author
    title: str
    tags: list[str] = None

    answers: list[AnswerReadDetailed] = None
    comments: list[CommentRead] = None


class QuestionUpdate(BaseModel):
    content: str
    title: str
    tags: list[str] = None
