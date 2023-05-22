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
filter .id = <uuid>$comment_id