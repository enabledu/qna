"use client";
import * as React from "react";
import { ThemeProvider } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import QuestionAnswerIcon from "@mui/icons-material/QuestionAnswer";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import { Box, Container } from "@mui/system";
import { Button } from "@mui/material";
import styles from "./posts.module.css";
// import theme from "@/app/config/theme";
import theme from "@/config/theme";
import { useState, useEffect } from "react";

var p;
var id;

const MainPosts = ({ posts, setActive }) => {
  const clickHandler = (e) => {
    id = e.target.getAttribute("data-index");
    setActive(true, id);
  };

  return (
    <>
      <ThemeProvider theme={theme}>
        <main className={styles.main}>
          <Typography variant="h3" className={styles.header} color={"primary"}>
            <QuestionAnswerIcon className={styles.icon} color={"primary"} />
            Posts
          </Typography>
          <Container className={styles.cont}>
            {posts.map((e) => {
              return (
                <>
                  <Box className={styles.question}>
                    <Button
                      data-index={e.id}
                      className={styles.questionHead}
                      onClick={clickHandler}
                      color="primary"
                      endIcon={
                        <ArrowForwardIosIcon
                          style={{
                            fontSize: "clamp(0.5rem, 2rem, 3rem)",
                            color: "primary",
                          }}
                        />
                      }
                    >
                      {e.title}
                    </Button>
                  </Box>
                </>
              );
            })}
          </Container>
        </main>
      </ThemeProvider>
    </>
  );
};

export default MainPosts;
