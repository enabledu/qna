with
  author := (
    select User
    filter .id = <uuid>$author_id
  ),
  comment := (
    insert Comment {
      author := author,
      content := <str>$content,
    }
  ),
  updated_question := (
    update Question
    filter .id = <uuid>$question_id
    set {
      comments += comment
    }
  )
select comment