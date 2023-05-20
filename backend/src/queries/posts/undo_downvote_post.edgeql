with
  downvoter := (
    select User
    filter .id = <uuid>$downvoter_id
  )
update Post
filter .id = <uuid>$post_id
set {
  downvotes := .downvotes-1,
  downvoters -= downvoter
}