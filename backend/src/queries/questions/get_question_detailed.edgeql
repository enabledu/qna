select Question {
  id,
  author: {
    id,
    username
  },
  title,
  content,
  tags,
  views,
  upvotes,
  downvotes,

  answers: {
    id,
    author: {
      id,
      username
    },
    content,
    upvotes,
    downvotes,
    is_accepted,
    comments: {
      id,
      author: {
        id,
        username
      },
      content,
      upvotes,
      downvotes,
    }
  },

  comments: {
    id,
    author: {
      id,
      username
    },
    content,
    upvotes,
    downvotes,
  }
}
filter .id = <uuid>$question_id