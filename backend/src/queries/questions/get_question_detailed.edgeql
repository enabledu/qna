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
  date_created,
  date_modified,

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
    date_created,
    date_modified
  }
}
filter .id = <uuid>$question_id