"use client";
import {
  Divider,
  Avatar,
  Grid,
  Paper,
  Button,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
// import theme from "@/app/config/theme";
import theme from "@/config/theme";
import { ThemeProvider } from "@emotion/react";
import axios from "axios";

const imgLink =
  "https://pixlok.com/wp-content/uploads/2022/02/Profile-Icon-SVG-09856789.png";

function Post({ postData }) {
  const [vote, setVote] = useState(0);
  const [author, setAuthor] = useState();

  const upVote = () => {
    setVote((v) => v + 1);
  };

  const downVote = () => {
    if (vote > 0) {
      setVote((v) => v - 1);
    } else {
      setVote(0);
    }
  };

  useEffect(() => {
    // if (postData.author.id != "") {
    //   console.log(postData.author.id);
    //   const address = `http://127.0.0.1:8000/users/${postData.author.id}`;
    //   axios.get(address, { mode: "no-cors" }).then((res) => {
    //     console.log(res.data);
    //     // setPosts(res.data);
    //   });
    // }
    // console.log(postData);

    setAuthor("Shedo");
  }, [postData]);
  return (
    <ThemeProvider theme={theme}>
      <Typography fontSize={26}>
        {/* This is a question header */}
        {postData.title || ""}
      </Typography>
      <Divider variant="fullWidth" style={{ margin: "5px 0 30px 0" }} />
      <Grid container wrap="nowrap" spacing={2}>
        <Grid item>
          <Avatar alt="Remy Sharp" src={imgLink} />
        </Grid>
        <Grid justifyContent="left" item xs zeroMinWidth>
          <div style={{ display: "flex", padding: "7px 0" }}>
            <h4 style={{ margin: 0, textAlign: "left" }}>{author}</h4>
            <p
              style={{
                textAlign: "left",
                color: "gray",
                margin: "0px",
                marginLeft: "6px",
              }}
            >
              1min ago
            </p>
          </div>
          <p style={{ textAlign: "left" }}>
            {/* Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean
            luctus ut est sed faucibus. Duis bibendum ac ex vehicula laoreet.
            Suspendisse congue vulputate lobortis. Pellentesque at interdum
            tortor. Quisque arcu quam, malesuada vel mauris et, posuere sagittis
            ipsum. Aliquam ultricies a ligula nec faucibus. In elit metus,
            efficitur lobortis nisi quis, molestie porttitor metus. Pellentesque
            et neque risus. Aliquam vulputate, mauris vitae tincidunt interdum,
            mauris mi vehicula urna, nec feugiat quam lectus vitae ex.
            Pellentesque et neque risus. Aliquam vulputate, mauris vitae
            tincidunt interdum, mauris mi vehicula urna, nec feugiat quam lectus
            vitae ex. Pellentesque et neque risus. Aliquam vulputate, mauris
            vitae tincidunt interdum, mauris mi vehicula urna, nec feugiat quam
            lectus vitae ex.Pellentesque et neque risus. Aliquam vulputate,
            mauris vitae tincidunt interdum, mauris mi vehicula urna, nec
            feugiat quam lectus vitae ex.Pellentesque et neque risus. Aliquam
            vulputate, mauris vitae tincidunt interdum, mauris mi vehicula urna,
            nec feugiat quam lectus vitae ex. */}

            {postData.content || ""}
          </p>
        </Grid>
      </Grid>
    </ThemeProvider>
  );
}

export default Post;
