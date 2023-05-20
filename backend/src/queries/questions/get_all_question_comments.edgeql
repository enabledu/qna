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
  downvotes
}