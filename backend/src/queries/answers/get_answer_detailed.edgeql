select Answer {
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
  date_modified,
  comments: {
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
}
filter .id = <uuid>$answer_id