select Answer {
  id,
  author: {
    id,
    username
  },
  content,
  upvotes,
  downvotes,
  is_accepted
}
filter .id = <uuid>$answer_id