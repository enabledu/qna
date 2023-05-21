from __future__ import annotations
import edgedb
import uuid

from qna.backend.src.models import PostID, QuestionRead, AnswerRead, CommentRead


async def accept_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    answer_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        with
          answer := (
            select Answer
            filter .id = <uuid>$answer_id
          ),
          question := (
            select answer.<answers[is Question]
          ),
          question_answers := (
            for answer in question.answers
            union (
              update answer
              set {
                is_accepted := false
              }
            )
          )
        update answer
        set {
          is_accepted := true
        }
        """,
        answer_id=answer_id,
    )


async def add_answer_to_question(
    executor: edgedb.AsyncIOExecutor,
    *,
    author_id: uuid.UUID,
    content: str,
    question_id: uuid.UUID,
) -> PostID:
    return await executor.query_single(
        """\
        with
          author := (
            select User
            filter .id = <uuid>$author_id
          ),
          answer := (
            insert Answer {
              author := author,
              content := <str>$content,
            }
          ),
          updated_question := (
            update Question
            filter .id = <uuid>$question_id
            set {
              answers += answer
            }
          )
        select answer\
        """,
        author_id=author_id,
        content=content,
        question_id=question_id,
    )


async def add_comment_to_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    author_id: uuid.UUID,
    content: str,
    answer_id: uuid.UUID,
) -> PostID:
    return await executor.query_single(
        """\
        with
          author := (
            select User
            filter .id = <uuid>$author_id
          ),
          comment := (
            insert Comment {
              author := author,
              content := <str>$content,
            }
          ),
          updated_answer := (
            update Answer
            filter .id = <uuid>$answer_id
            set {
              comments += comment
            }
          )
        select comment\
        """,
        author_id=author_id,
        content=content,
        answer_id=answer_id,
    )


async def add_comment_to_question(
    executor: edgedb.AsyncIOExecutor,
    *,
    author_id: uuid.UUID,
    content: str,
    question_id: uuid.UUID,
) -> PostID:
    return await executor.query_single(
        """\
        with
          author := (
            select User
            filter .id = <uuid>$author_id
          ),
          comment := (
            insert Comment {
              author := author,
              content := <str>$content,
            }
          ),
          updated_question := (
            update Question
            filter .id = <uuid>$question_id
            set {
              comments += comment
            }
          )
        select comment\
        """,
        author_id=author_id,
        content=content,
        question_id=question_id,
    )


async def add_question(
    executor: edgedb.AsyncIOExecutor,
    *,
    author_id: uuid.UUID,
    title: str,
    content: str,
    tags: list[str] | None,
) -> PostID:
    return await executor.query_single(
        """\
        insert Question {
          author := (
            select User
            filter .id = <uuid>$author_id
          ),
          title := <str>$title,
          content := <str>$content,
          tags := <optional array<str>>$tags
        }\
        """,
        author_id=author_id,
        title=title,
        content=content,
        tags=tags,
    )


async def delete_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    answer_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        delete Answer
        filter .id = <uuid>$answer_id\
        """,
        answer_id=answer_id,
    )


async def delete_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    comment_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        delete Comment
        filter .id = <uuid>$comment_id\
        """,
        comment_id=comment_id,
    )


async def delete_question(
    executor: edgedb.AsyncIOExecutor,
    *,
    question_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        delete Question
        filter .id = <uuid>$question_id\
        """,
        question_id=question_id,
    )


async def downvote_post(
    executor: edgedb.AsyncIOExecutor,
    *,
    downvoter_id: uuid.UUID,
    post_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        with
          downvoter := (
            select User
            filter .id = <uuid>$downvoter_id
          ),
          post := (
            update Post
            filter .id = <uuid>$post_id
            set {
              upvoters -= downvoter,
              downvoters += downvoter
            }
          )
        select post {
          id,
          upvotes,
          downvotes,
        }
        """,
        downvoter_id=downvoter_id,
        post_id=post_id,
    )


async def edit_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    answer_id: uuid.UUID,
    content: str,
) -> PostID | None:
    return await executor.query_single(
        """\
        with date_modified := datetime_of_statement()
        update Answer
        filter .id = <uuid>$answer_id
        set {
          content := <str>$content,
          date_modified := date_modified
        }
        """,
        answer_id=answer_id,
        content=content,
    )


async def edit_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    comment_id: uuid.UUID,
    content: str,
) -> PostID | None:
    return await executor.query_single(
        """\
        with date_modified := datetime_of_statement()
        update Comment
        filter .id = <uuid>$comment_id
        set {
            content := <str>$content,
            date_modified := date_modified
        }
        """,
        comment_id=comment_id,
        content=content,
    )


async def edit_question(
    executor: edgedb.AsyncIOExecutor,
    *,
    question_id: uuid.UUID,
    title: str,
    content: str,
    tags: list[str] | None,
) -> PostID | None:
    return await executor.query_single(
        """\
        with date_modified := datetime_of_statement()
        update Question
        filter .id = <uuid>$question_id
        set {
          title := <str>$title,
          content := <str>$content,
          tags := <optional array <str>>$tags,
          date_modified := date_modified
        }
        """,
        question_id=question_id,
        title=title,
        content=content,
        tags=tags,
    )


async def get_all_answer_comments(
    executor: edgedb.AsyncIOExecutor,
    *,
    answer_id: uuid.UUID,
) -> list[CommentRead]:
    return await executor.query(
        """\
        with answer := (
          select Answer
          filter .id = <uuid>$answer_id
        )
        select answer.comments {
          id,
          author: {
            id,
            username
          },
          content,
          upvotes,
          downvotes,
          date_created,
          date_modified
        }
        order by .date_created
        """,
        answer_id=answer_id,
    )


async def get_all_question_answers(
    executor: edgedb.AsyncIOExecutor,
    *,
    question_id: uuid.UUID,
) -> list[AnswerRead]:
    return await executor.query(
        """\
        with question := (
          select Question
          filter .id = <uuid>$question_id
        )
        select question.answers {
          id,
          author: {
            id,
            username
          },
          content,
          upvotes,
          downvotes,
          is_accepted,
          date_created,
          date_modified
        }
        order by .date_created
        """,
        question_id=question_id,
    )


async def get_all_question_comments(
    executor: edgedb.AsyncIOExecutor,
    *,
    question_id: uuid.UUID,
) -> list[CommentRead]:
    return await executor.query(
        """\
        with question := (
          select Question
          filter .id = <uuid>$question_id
        )
        select question.comments {
          id,
          author: {
            id,
            username
          },
          content,
          upvotes,
          downvotes,
          date_created,
          date_modified
        }
        order by .date_created
        """,
        question_id=question_id,
    )


async def get_all_questions(
    executor: edgedb.AsyncIOExecutor,
) -> list[QuestionRead]:
    return await executor.query(
        """\
        select Question {
          id,
          author: {
            id,
            username
          },
          title,
          content,
          tags,
          views,
          upvotes,
          downvotes,
          date_created,
          date_modified
        }
        order by .date_created desc
        """,
    )


async def get_answer_detailed(
    executor: edgedb.AsyncIOExecutor,
    *,
    answer_id: uuid.UUID,
) -> AnswerRead | None:
    return await executor.query_single(
        """\
        select Answer {
          id,
          author: {
            id,
            username
          },
          content,
          upvotes,
          downvotes,
          is_accepted,
          date_created,
          date_modified,
        
          comments: {
            id,
            author: {
              id,
              username
            },
            content,
            upvotes,
            downvotes,
            date_created,
            date_modified
          }
        }
        filter .id = <uuid>$answer_id
        """,
        answer_id=answer_id,
    )


async def get_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    answer_id: uuid.UUID,
) -> AnswerRead | None:
    return await executor.query_single(
        """\
        select Answer {
          id,
          author: {
            id,
            username
          },
          content,
          upvotes,
          downvotes,
          is_accepted,
          date_created,
          date_modified
        }
        filter .id = <uuid>$answer_id\
        """,
        answer_id=answer_id,
    )


async def get_comment(
    executor: edgedb.AsyncIOExecutor,
    *,
    comment_id: uuid.UUID,
) -> CommentRead | None:
    return await executor.query_single(
        """\
        select Comment {
          id,
          author: {
            id,
            username
          },
          content,
          upvotes,
          downvotes,
          date_created,
          date_modified
        }
        filter .id = <uuid>$comment_id\
        """,
        comment_id=comment_id,
    )


async def get_question(
    executor: edgedb.AsyncIOExecutor,
    *,
    question_id: uuid.UUID,
) -> QuestionRead | None:
    return await executor.query_single(
        """\
        select Question {
          id,
          author: {
            id,
            username
          },
          title,
          content,
          tags,
          views,
          upvotes,
          downvotes,
          date_created,
          date_modified
        }
        filter .id = <uuid>$question_id\
        """,
        question_id=question_id,
    )


async def get_question_detailed(
    executor: edgedb.AsyncIOExecutor,
    *,
    question_id: uuid.UUID,
) -> QuestionRead | None:
    return await executor.query_single(
        """\
        select Question {
          id,
          author: {
            id,
            username
          },
          title,
          content,
          tags,
          views,
          upvotes,
          downvotes,
          date_created,
          date_modified,
        
          answers: {
            id,
            author: {
              id,
              username
            },
            content,
            upvotes,
            downvotes,
            is_accepted,
            date_created,
            date_modified,
            comments: {
              id,
              author: {
                id,
                username
              },
              content,
              upvotes,
              downvotes,
              date_created,
              date_modified
            }
          },
        
          comments: {
            id,
            author: {
              id,
              username
            },
            content,
            upvotes,
            downvotes,
            date_created,
            date_modified
          }
        }
        filter .id = <uuid>$question_id
        """,
        question_id=question_id,
    )


async def increment_question_views(
    executor: edgedb.AsyncIOExecutor,
    *,
    question_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        update Question
        filter .id = <uuid>$question_id
        set {
          views := .views+1
        }
        """,
        question_id=question_id,
    )


async def undo_accept_answer(
    executor: edgedb.AsyncIOExecutor,
    *,
    answer_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        update Answer
        filter .id = <uuid>$answer_id
        set {
            is_accepted := false
        }\
        """,
        answer_id=answer_id,
    )


async def undo_downvote_post(
    executor: edgedb.AsyncIOExecutor,
    *,
    downvoter_id: uuid.UUID,
    post_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        with
          downvoter := (
            select User
            filter .id = <uuid>$downvoter_id
          ),
          post := (
            update Post
            filter .id = <uuid>$post_id
            set {
              downvoters -= downvoter
            }
          )
        select post {
          id,
          upvotes,
          downvotes
        }
        """,
        downvoter_id=downvoter_id,
        post_id=post_id,
    )


async def undo_upvote_post(
    executor: edgedb.AsyncIOExecutor,
    *,
    upvoter_id: uuid.UUID,
    post_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        with
          upvoter := (
            select User
            filter .id = <uuid>$upvoter_id
          ),
          post := (
            update Post
            filter .id = <uuid>$post_id
            set {
              upvoters -= upvoter
            }
          )
        select post {
          id,
          upvotes,
          downvotes
        }
        """,
        upvoter_id=upvoter_id,
        post_id=post_id,
    )


async def upvote_post(
    executor: edgedb.AsyncIOExecutor,
    *,
    upvoter_id: uuid.UUID,
    post_id: uuid.UUID,
) -> PostID | None:
    return await executor.query_single(
        """\
        with
          upvoter := (
            select User
            filter .id = <uuid>$upvoter_id
          ),
          post := (
            update Post
            filter .id = <uuid>$post_id
            set {
              downvoters -= upvoter,
              upvoters += upvoter
            }
          )
        select post {
          id,
          upvotes,
          downvotes
        }\
        """,
        upvoter_id=upvoter_id,
        post_id=post_id,
    )
