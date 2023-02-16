update Comment
filter .id = <uuid>$id
set{
    upvote := .upvote+1
}