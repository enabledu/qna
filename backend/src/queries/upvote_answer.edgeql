update Answer
filter .id = <uuid>$id
set{
    upvote := .upvote+1
}