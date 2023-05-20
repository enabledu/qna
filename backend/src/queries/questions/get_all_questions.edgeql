select Question {
  id,
  author: {
    id,
    username
  },
  title,
  content,
  upvotes,
  downvotes,
}