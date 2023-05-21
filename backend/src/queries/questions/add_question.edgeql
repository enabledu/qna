insert Question {
  author := (
    select User
    filter .id = <uuid>$author_id
  ),
  title := <str>$title,
  content := <str>$content,
  tags := <optional array<str>>$tags
}