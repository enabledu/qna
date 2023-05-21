with
  upvoter := (
    select User
    filter .id = <uuid>$upvoter_id
  ),
  post := (
    update Post
    filter .id = <uuid>$post_id
    set {
      downvoters -= upvoter,
      upvoters += upvoter
    }
  )
select post {
  id,
  upvotes,
  downvotes
}
