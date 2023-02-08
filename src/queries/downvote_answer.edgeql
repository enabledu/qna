update Answer
filter .id = <uuid>$id
set{
    downvote := .downvote+1
}