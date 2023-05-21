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
  updated_answer := (
    update Answer
    filter .id = <uuid>$answer_id
    set {
      comments += comment
    }
  )
select comment