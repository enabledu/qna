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