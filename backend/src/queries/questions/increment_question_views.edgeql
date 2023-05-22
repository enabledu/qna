update Question
filter .id = <uuid>$question_id
set {
  views := .views+1
}