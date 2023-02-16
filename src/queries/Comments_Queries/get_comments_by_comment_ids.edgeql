select Comment{
  content,
  upvote,
  downvote,
  author
} filter .id in array_unpack(<array<uuid>>$ids)