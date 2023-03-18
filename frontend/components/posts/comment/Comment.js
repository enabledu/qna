"use client";
import {
  Divider,
  Avatar,
  Grid,
  Paper,
  Button,
  Typography,
} from "@mui/material";
import { useState } from "react";
// import theme from "@/app/config/theme";
import theme from "@/config/theme";
import { ThemeProvider } from "@emotion/react";
import ArrowDropUpIcon from "@mui/icons-material/ArrowDropUp";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";

const imgLink =
  "https://pixlok.com/wp-content/uploads/2022/02/Profile-Icon-SVG-09856789.png";
function Comment({ data }) {
  const [vote, setVote] = useState(0);

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
  const counter = useState();
  return (
    <ThemeProvider theme={theme}>
      <Grid container wrap="nowrap" spacing={2}>
        <Grid
          item
          style={{
            display: "flex",
            flexDirection: "column",
          }}
        >
          <Button variant="text" color="primary" onClick={upVote}>
            <ArrowDropUpIcon />
          </Button>
          <Typography style={{ textAlign: "center" }} color="primary">
            {vote}
          </Typography>
          <Button variant="text" color="primary" onClick={downVote}>
            <ArrowDropDownIcon />
          </Button>
        </Grid>
        <Grid item>
          <Avatar alt="Remy Sharp" src={imgLink} />
        </Grid>
        <Grid justifyContent="left" item xs zeroMinWidth>
          <div style={{ display: "flex", padding: "7px 0" }}>
            <h4 style={{ margin: 0, textAlign: "left" }}>{"author"}</h4>
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
          <p style={{ textAlign: "left" }}>{data.content || ""}</p>
        </Grid>
      </Grid>
    </ThemeProvider>
  );
}

export default Comment;
