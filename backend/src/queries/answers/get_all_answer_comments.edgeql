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