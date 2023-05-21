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
order by .date_created desc