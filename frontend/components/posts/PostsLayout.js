"use client";
import {
  Divider,
  Avatar,
  Grid,
  Paper,
  Button,
  Typography,
  TextField,
} from "@mui/material";
import { useState, useRef, useEffect } from "react";
// import theme from "@/app/config/theme";
import theme from "@/config/theme";
import { ThemeProvider } from "@emotion/react";
import Comment from "./comment/Comment";
import Post from "./Posts/Post";
import * as React from "react";
import Dialog from "@mui/material/Dialog";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import Slide from "@mui/material/Slide";
import SendIcon from "@mui/icons-material/Send";
import { getFromStorage } from "@/helpers/localStorage";

const imgLink =
  "https://pixlok.com/wp-content/uploads/2022/02/Profile-Icon-SVG-09856789.png";

const author_id = getFromStorage("user_id");

function PostLayout({ postData, setCommentsAdded }) {
  const comment = useRef();
  const sendComment = () => {
    var formBody = [];
    let body = {
      question_id: postData.id,
      author_id: author_id,
      content: comment.current.value,
    };
    for (let property in body) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(body[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    console.log(formBody);
    let address = `http://127.0.0.1:8000/qna_app/question/${postData.id}/answer/add?${formBody}`;
    console.log(address);

    fetch(address, {
      method: "POST",
      mode: "no-cors",
      header: {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }).then((res) => {
      console.log(res.data);
    });
    setCommentsAdded((prev) => prev + 1);
  };

  const counter = useState();
  return (
    <ThemeProvider theme={theme}>
      <main
        style={{
          padding: 14,
          backgroundColor: "#eef5f9",
          minHeight: "calc(100vh - 64px)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          overflow: "scroll",
        }}
      >
        <Paper
          style={{
            padding: "40px 20px",
            width: "clamp(250px, 50%, 900px)",
            maxWidth: "900px",
          }}
        >
          <Post postData={postData} />
        </Paper>
        <Typography
          color={theme.palette.textColor.main}
          fontSize={25}
          margin={3}
        >
          Comments
        </Typography>

        {postData.answer?.map((e) => {
          console.log(e);
          return (
            <>
              <Paper
                style={{
                  padding: "20px",
                  maxWidth: "900px",
                  width: "clamp(250px, 50%, 900px)",
                  margin: "6px 0",
                }}
              >
                <Comment data={e} />
              </Paper>
            </>
          );
        })}
        <Paper
          style={{
            padding: "20px",
            margin: "12px 0",
            maxWidth: "900px",
            width: "clamp(250px, 50%, 900px)",
          }}
        >
          <Grid
            container
            wrap="nowrap"
            spacing={0}
            style={{
              display: "grid",
              gridTemplateColumns: "40px auto 0.2fr",
            }}
          >
            <Avatar item alt="Remy Sharp" src={imgLink} />
            <TextField
              item
              id="input-with-sx"
              label="Write a comment"
              variant="outlined"
              multiline
              inputRef={comment}
              style={{ margin: " 0 12px" }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={sendComment}
              endIcon={<SendIcon />}
            >
              Send
            </Button>
          </Grid>
        </Paper>
      </main>
    </ThemeProvider>
  );
}

// Template from MUI

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="left" ref={ref} {...props} />;
});

const FullScreenDialog = ({ active, setActive, posts, setCommentsAdded }) => {
  const [postData, setPostData] = useState({
    title: "",
    content: "",
    id: "",
    author: { id: "" },
  });

  const handleClose = () => {
    setActive(false, "");
  };

  useEffect(() => {
    setPostData(
      posts.find((e) => e.id === active.id) || {
        title: "",
        content: "",
        id: "",
        author: { id: "" },
      }
    );
    console.log(postData);
  }, [active]);
  return (
    <ThemeProvider theme={theme}>
      <div>
        <Dialog
          fullScreen
          open={active.state}
          onClose={handleClose}
          TransitionComponent={Transition}
        >
          <AppBar sx={{ position: "relative" }} backgroundColor={"primary"}>
            <Toolbar>
              <IconButton
                edge="start"
                color="inherit"
                onClick={handleClose}
                aria-label="close"
              >
                <CloseIcon />
              </IconButton>
              <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
                Close
              </Typography>
            </Toolbar>
          </AppBar>
          <PostLayout postData={postData} setCommentsAdded={setCommentsAdded} />
        </Dialog>
      </div>
    </ThemeProvider>
  );
};

export default FullScreenDialog;
