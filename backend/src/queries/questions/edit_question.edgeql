with date_modified := datetime_of_statement()
update Question
filter .id = <uuid>$question_id
set {
  title := <str>$title,
  content := <str>$content,
  tags := <optional array <str>>$tags,
  date_modified := date_modified
}