with
  author := (
    select User
    filter .id = <uuid>$author_id
  ),
  answer := (
    insert Answer {
      author := author,
      content := <str>$content,
    }
  ),
  updated_question := (
    update Question
    filter .id = <uuid>$question_id
    set {
      answers += answer
    }
  )
select answer