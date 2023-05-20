from uuid import UUID

from pydantic import BaseModel


class Author(BaseModel):
    id: UUID
    username: str


class PostID(BaseModel):
    id: UUID


class Post(PostID, BaseModel):
    content: str
    upvotes: int = 0
    downvotes: int = 0
    author: Author


class Question(Post):
    title: str
    tags: list[str] = None


class Answer(Post):
    is_accepted: bool = False


class Comment(Post):
    pass
