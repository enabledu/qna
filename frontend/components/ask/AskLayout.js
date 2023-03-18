"use client";
import * as React from "react";
import { ThemeProvider } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import QuestionAnswerIcon from "@mui/icons-material/QuestionAnswer";
import { Box, Container } from "@mui/system";
import { Button, TextField } from "@mui/material";
import styles from "./ask.module.css";
// import theme from "@/app/config/theme";
import theme from "@/config/theme";
import { useState, useRef } from "react";
import MuiTags from "./Tags";

var p;
var id;

const AskLayout = ({ submitHandler, reset }) => {
  const title = useRef();
  const content = useRef();
  const [tags, setTags] = useState("");

  const submit = () => {
    let data = {
      title: title.current.value,
      content: content.current.value,
      tags: tags,
    };
    submitHandler(data);
  };

  const getTags = (e) => {
    setTags(e.join(" "));
    console.log(tags);
  };

  return (
    <>
      <ThemeProvider theme={theme}>
        <main className={styles.main}>
          <Typography variant="h3" className={styles.header} color={"primary"}>
            <QuestionAnswerIcon className={styles.icon} color={"primary"} />
            Ask A question
          </Typography>
          <Container className={styles.cont}>
            <Box className={styles.question}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="title"
                label="Title"
                name="title"
                autoComplete="title"
                autoFocus
                inputRef={title}
              />
            </Box>
            <Box className={styles.question}>
              <MuiTags tags={[]} getTags={getTags} />
            </Box>
            <Box className={styles.question}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="question"
                label="Question"
                name="question"
                autoComplete="question"
                autoFocus
                multiline
                rows={4}
                inputRef={content}
              />
            </Box>

            <Box>
              <Button
                variant="contained"
                color="primary"
                style={{ fontSize: "18px", margin: "12px 25px 12px 0" }}
                onClick={submit}
              >
                Ask Question
              </Button>
              <Button
                variant="outlined"
                color="primary"
                style={{ fontSize: "18px" }}
              >
                Discard
              </Button>
            </Box>
          </Container>
        </main>
      </ThemeProvider>
    </>
  );
};

export default AskLayout;
