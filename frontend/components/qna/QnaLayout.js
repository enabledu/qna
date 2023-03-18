"use client";
import * as React from "react";
import { ThemeProvider } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import QuestionAnswerIcon from "@mui/icons-material/QuestionAnswer";
import ControlPointIcon from "@mui/icons-material/ControlPoint";
import RemoveCircleOutlineIcon from "@mui/icons-material/RemoveCircleOutline";
import { Box, Container } from "@mui/system";
import { Button } from "@mui/material";
import styles from "./qna.module.css";
// import theme from "@/app/config/theme";
import theme from "@/config/theme";
import { useState, useEffect } from "react";
import $ from "jquery";

var p;
var id;

const QnaLayout = ({ questions }) => {
  const [active, setActive] = useState(false);
  const [activeId, setActiveId] = useState("");

  const clickHandler = (e) => {
    id = e.target.getAttribute("data-index");
    p = e.target.parentElement.children[1];
    setActive((prev) => !prev);
    // console.log(activeId);
  };

  useEffect(() => {
    if (!active) {
      $(p).animate({ height: 0 }, 200, () => {
        $(p).css({ margin: "0" });
      });
      setActiveId("");
    } else {
      $(p).css({ margin: "clamp(6px, 22px, 25px)" });
      $(p).animate({ height: $(p).get(0).scrollHeight }, 200);
      setActiveId(id);
    }
  }, [active]);

  useEffect;
  return (
    <>
      <ThemeProvider theme={theme}>
        <main className={styles.main}>
          <Typography variant="h3" className={styles.header} color={"primary"}>
            <QuestionAnswerIcon className={styles.icon} color={"primary"} />
            Frequently asked questions
          </Typography>
          <Container className={styles.cont}>
            {questions.map((e) => {
              return (
                <>
                  <Box className={styles.question}>
                    <Button
                      data-index={e.id}
                      className={styles.questionHead}
                      onClick={clickHandler}
                      color="primary"
                      endIcon={
                        activeId != e.id ? (
                          <ControlPointIcon
                            style={{
                              fontSize: "clamp(0.5rem, 2rem, 3rem)",
                              color: "textColor",
                            }}
                          />
                        ) : (
                          <RemoveCircleOutlineIcon
                            style={{
                              fontSize: "clamp(0.5rem, 2rem, 3rem)",
                              color: "primary",
                            }}
                          />
                        )
                      }
                    >
                      {e.question}
                    </Button>
                    <Typography
                      className={styles.questionBody}
                      color={theme.palette.textColor.main}
                    >
                      {e.answer}
                    </Typography>
                  </Box>
                  ;
                </>
              );
            })}
          </Container>
        </main>
      </ThemeProvider>
    </>
  );
};

export default QnaLayout;
