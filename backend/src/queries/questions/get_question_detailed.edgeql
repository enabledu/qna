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

  answers := (
    select .answers {
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
      comments := (
        select .comments {
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
        } order by .date_created
      )
    } order by .date_created
  ),


  comments := (
    select .comments {
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
    } order by .date_created
  )
}
filter .id = <uuid>$question_id