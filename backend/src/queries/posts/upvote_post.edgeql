with
  upvoter := (
    select User
    filter .id = <uuid>$upvoter_id
  )
update Post
filter .id = <uuid>$post_id
set {
  upvotes := .upvotes+1,
  upvoters += upvoter
}