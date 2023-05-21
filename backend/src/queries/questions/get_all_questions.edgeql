select Question {
  id,
  author: {
    id,
    username
  },
  title,
  content,
  tags,
  upvotes,
  downvotes,
}