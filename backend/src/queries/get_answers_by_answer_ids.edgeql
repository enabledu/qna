select Answer{
  content,
  upvote,
  downvote,
  author,
  comments,
  is_accepted
} filter .id in array_unpack(<array<uuid>>$ids)