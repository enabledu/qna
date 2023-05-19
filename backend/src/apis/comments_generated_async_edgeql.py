# AUTOGENERATED FROM:
#     'apps/qna_app/backend/src/queries/accept_answer.edgeql'
#     'apps/qna_app/backend/src/queries/delete_answer.edgeql'
#     'apps/qna_app/backend/src/queries/comments/delete_comment.edgeql'
#     'apps/qna_app/backend/src/queries/downvote_answer.edgeql'
#     'apps/qna_app/backend/src/queries/comments/downvote_comment.edgeql'
#     'apps/qna_app/backend/src/queries/edit_answer.edgeql'
#     'apps/qna_app/backend/src/queries/comments/edit_comment.edgeql'
#     'apps/qna_app/backend/src/queries/get_all_answers.edgeql'
#     'apps/qna_app/backend/src/queries/comments/get_all_comments.edgeql'
#     'apps/qna_app/backend/src/queries/get_answers_by_answer_ids.edgeql'
#     'apps/qna_app/backend/src/queries/comments/get_comments_by_comment_ids.edgeql'
#     'apps/qna_app/backend/src/queries/get_all_answer_comments.edgeql'
#     'apps/qna_app/backend/src/queries/undo_accept_answer.edgeql'
#     'apps/qna_app/backend/src/queries/undo_downvote_answer.edgeql'
#     'apps/qna_app/backend/src/queries/comments/undo_downvote_comment.edgeql'
#     'apps/qna_app/backend/src/queries/undo_upvote_answer.edgeql'
#     'apps/qna_app/backend/src/queries/comments/undo_upvote_comment.edgeql'
#     'apps/qna_app/backend/src/queries/upvote_answer.edgeql'
#     'apps/qna_app/backend/src/queries/comments/upvote_comment.edgeql'
# WITH:
#     $ edgedb-py --file --no-skip-pydantic-validation


from __future__ import annotations
import dataclasses
import edgedb
import uuid


@dataclasses.dataclass
class AcceptAnswerResult:
    id: uuid.UUID


@dataclasses.dataclass
class DeleteCommentResult:
    id: uuid.UUID


@dataclasses.dataclass
class GetAllAnswersResult:
    id: uuid.UUID
    content: str
    upvote: int | None
    downvote: int | None
    author: GetAllAnswersResultAuthor
    comments: list[DeleteCommentResult]
    is_accepted: bool | None


@dataclasses.dataclass
class GetAllAnswersResultAuthor:
    id: uuid.UUID


@dataclasses.dataclass
class GetAllCommentsResult:
    id: uuid.UUID
    content: str
    upvote: int | None
    downvote: int | None
    author: GetAllAnswersResultAuthor


async def accept_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """\
        update Answer
        filter .id = <uuid>$id
        set{
            is_accepted := true
        }\
        """,
        id=id,
    )


async def delete_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """\
        delete Answer
        filter .id = <uuid>$id\
        """,
        id=id,
    )


async def delete_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> DeleteCommentResult | None:
    return await executor.query_single(
        """\
        delete Comment
        filter .id = <uuid>$id\
        """,
        id=id,
    )


async def downvote_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """\
        update Answer
        filter .id = <uuid>$id
        set{
            downvote := .downvote+1
        }\
        """,
        id=id,
    )


async def downvote_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> DeleteCommentResult | None:
    return await executor.query_single(
        """\
        update Comment
        filter .id = <uuid>$id
        set{
            downvote := .downvote+1
        }\
        """,
        id=id,
    )


async def edit_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
    content: str,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """\
        update Answer
        filter .id = <uuid>$id
        set{
            content := <str>$content
        }\
        """,
        id=id,
        content=content,
    )


async def edit_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
    content: str,
) -> DeleteCommentResult | None:
    return await executor.query_single(
        """\
        update Comment
        filter .id = <uuid>$id
        set{
            content := <str>$content
        }\
        """,
        id=id,
        content=content,
    )


async def get_all_answers(
    executor: edgedb.AsyncIOExecutor,
) -> list[GetAllAnswersResult]:
    return await executor.query(
        """\
        select Answer{
          content,
          upvote,
          downvote,
          author,
          comments,
          is_accepted
        }\
        """,
    )


async def get_all_comments(
    executor: edgedb.AsyncIOExecutor,
) -> list[GetAllCommentsResult]:
    return await executor.query(
        """\
        select Comment{
          content,
          upvote,
          downvote,
          author,

        }\
        """,
    )


async def get_answers_by_answer_ids(
    executor: edgedb.AsyncIOExecutor,
    *,
    ids: list[uuid.UUID],
) -> list[GetAllAnswersResult]:
    return await executor.query(
        """\
        select Answer{
          content,
          upvote,
          downvote,
          author,
          comments,
          is_accepted
        } filter .id in array_unpack(<array<uuid>>$ids)\
        """,
        ids=ids,
    )


async def get_comments_by_comment_ids(
    executor: edgedb.AsyncIOExecutor,
    *,
    ids: list[uuid.UUID],
) -> list[GetAllCommentsResult]:
    return await executor.query(
        """\
        select Comment{
          content,
          upvote,
          downvote,
          author
        } filter .id in array_unpack(<array<uuid>>$ids)\
        """,
        ids=ids,
    )


async def get_comments_on_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> list[GetAllCommentsResult]:
    return await executor.query(
        """\
        with comment_ids := (select Answer filter .id = <uuid>$id)
        select Comment{
          content,
          upvote,
          downvote,
          author
        } filter .id in comment_ids.comments.id\
        """,
        id=id,
    )


async def undo_accept_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """\
        update Answer
        filter .id = <uuid>$id
        set{
            is_accepted := false
        }\
        """,
        id=id,
    )


async def undo_downvote_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """\
        update Answer
        filter .id = <uuid>$id
        set{
            downvote := .downvote-1
        }\
        """,
        id=id,
    )


async def undo_downvote_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> DeleteCommentResult | None:
    return await executor.query_single(
        """\
        update Comment
        filter .id = <uuid>$id
        set{
            downvote := .downvote-1
        }\
        """,
        id=id,
    )


async def undo_upvote_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """\
        update Answer
        filter .id = <uuid>$id
        set{
            upvote := .upvote-1
        }\
        """,
        id=id,
    )


async def undo_upvote_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> DeleteCommentResult | None:
    return await executor.query_single(
        """\
        update Comment
        filter .id = <uuid>$id
        set{
            upvote := .upvote-1
        }\
        """,
        id=id,
    )


async def upvote_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> AcceptAnswerResult | None:
    return await executor.query_single(
        """\
        update Answer
        filter .id = <uuid>$id
        set{
            upvote := .upvote+1
        }\
        """,
        id=id,
    )


async def upvote_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> DeleteCommentResult | None:
    return await executor.query_single(
        """\
        update Comment
        filter .id = <uuid>$id
        set{
            upvote := .upvote+1
        }\
        """,
        id=id,
    )
