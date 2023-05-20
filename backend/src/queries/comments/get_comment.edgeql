select Comment {
  id,
  author: {
    id,
    username
  },
  content,
  upvotes,
  downvotes,
}
filter .id = <uuid>$comment_id