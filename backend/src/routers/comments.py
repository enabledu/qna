import dataclasses
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from enabled.backend.src.database import get_client
from qna.backend.src import queries

from qna.backend.src.models import (CommentCreate, CommentRead, CommentUpdate,
                                    PostID, PostVote, ErrorModel)

from enabled.backend.src.users.users import current_active_user

from qna.backend.src.dependencies import get_comment

comments_router = APIRouter(tags=["qna: comments"], prefix="/comment")


@comments_router.post("/{comment_id}/edit/",
                      responses={404: {"model": ErrorModel},
                                 403: {"model": ErrorModel}})
async def edit_comment(comment_id: UUID,
                       update_comment: CommentUpdate,
                       comment: CommentRead = Depends(get_comment),
                       user=Depends(current_active_user),
                       client=Depends(get_client)) -> PostID:
    if not comment.author.id == user.id:
        raise HTTPException(status_code=403, detail="ONLY_COMMENT_AUTHOR_CAN_EDIT_IT")
    else:
        comment_dict = dataclasses.asdict(comment)
        comment_dict.update(update_comment.dict())
        update_comment = {k: v
                          for k, v in comment_dict.items()
                          if k in ['content']}
        return await queries.edit_comment(client, comment_id=comment_id, **update_comment)


@comments_router.post("/{comment_id}/delete/",
                      responses={404: {"model": ErrorModel},
                                 403: {"model": ErrorModel}})
async def delete_comment(comment_id: UUID,
                         comment: CommentRead = Depends(get_comment),
                         user=Depends(current_active_user),
                         client=Depends(get_client)) -> PostID:
    if not comment.author.id == user.id:
        raise HTTPException(status_code=403, detail="ONLY_COMMENT_AUTHOR_CAN_DELETE_IT")
    else:
        return await queries.delete_comment(client, comment_id=comment_id)


@comments_router.post("/{comment_id}/upvote/",
                      dependencies=[Depends(get_comment)],
                      responses={404: {"model": ErrorModel}})
async def upvote_comment(comment_id: UUID,
                         user=Depends(current_active_user),
                         client=Depends(get_client)) -> PostVote:
    return await queries.upvote_post(client,
                                     post_id=comment_id,
                                     upvoter_id=user.id)


@comments_router.post("/{comment_id}/upvote/undo/",
                      dependencies=[Depends(get_comment)],
                      responses={404: {"model": ErrorModel}})
async def undo_upvote_comment(comment_id: UUID,
                              user=Depends(current_active_user),
                              client=Depends(get_client)) -> PostVote:
    return await queries.undo_upvote_post(client,
                                          post_id=comment_id,
                                          upvoter_id=user.id)


@comments_router.post("/{comment_id}/downvote/",
                      dependencies=[Depends(get_comment)],
                      responses={404: {"model": ErrorModel}})
async def downvote_comment(comment_id: UUID,
                           user=Depends(current_active_user),
                           client=Depends(get_client)) -> PostVote:
    return await queries.downvote_post(client,
                                       post_id=comment_id,
                                       downvoter_id=user.id)


@comments_router.post("/{comment_id}/downvote/undo/",
                      dependencies=[Depends(get_comment)],
                      responses={404: {"model": ErrorModel}})
async def undo_downvote_comment(comment_id: UUID,
                                user=Depends(current_active_user),
                                client=Depends(get_client)) -> PostVote:
    return await queries.undo_downvote_post(client,
                                            post_id=comment_id,
                                            downvoter_id=user.id)
