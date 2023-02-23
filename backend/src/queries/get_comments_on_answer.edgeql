with comment_ids := (select Answer filter .id = <uuid>$id)
select Comment{
  content,
  upvote,
  downvote,
  author
} filter .id in comment_ids.comments.id