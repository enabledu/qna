select Question {
  id,
  author: {
    id,
    username
  },
  title,
  content,
  upvotes,
  downvotes,
}
filter .id = <uuid>$question_id