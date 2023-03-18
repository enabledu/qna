"use client";
import PostsLayout from "./PostsLayout";
import MainPosts from "./MainPosts";
import Post from "./Posts/Post";
import FullScreenDialog from "./PostsLayout";
import { useEffect, useState } from "react";
import axios from "axios";
const posts_list = [
  {
    id: "123456",
    header: "lol this is a question header",
  },
];

const Posts = () => {
  const [active, setActive] = useState({ state: false, id: "" });
  const [posts, setPosts] = useState(posts_list);
  const [commentsAdded, setCommentsAdded] = useState(0);
  const openDialog = (state, id) => {
    setActive({ state: state, id: id });
  };
  const address = `http://127.0.0.1:8000/qna_app/question/all`;

  useEffect(() => {
    axios.get(address, { mode: "no-cors" }).then((res) => {
      console.log(res.data);
      setPosts(res.data);
    });
  }, [address, commentsAdded]);
  return (
    <>
      <main
        style={{
          "& *": { fontFamily: `"Roboto", "Helvetica", "Arial", sans-serif` },
        }}
      >
        <MainPosts posts={posts} setActive={openDialog} />
        <main>
          <FullScreenDialog
            active={active}
            setActive={openDialog}
            posts={posts}
            setCommentsAdded={setCommentsAdded}
          />
        </main>
      </main>
    </>
  );
};

export default Posts;
