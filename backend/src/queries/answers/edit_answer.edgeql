with date_modified := datetime_of_statement()
update Answer
filter .id = <uuid>$answer_id
set {
  content := <str>$content,
  date_modified := date_modified
}