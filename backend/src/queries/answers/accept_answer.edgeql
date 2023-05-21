with
  answer := (
    select Answer
    filter .id = <uuid>$answer_id
  ),
  question := (
    select answer.<answers[is Question]
  ),
  question_answers := (
    for answer in question.answers
    union (
      update answer
      set {
        is_accepted := false
      }
    )
  )
update answer
set {
  is_accepted := true
}
