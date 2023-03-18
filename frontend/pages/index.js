import GroupsNav from "@/components/GroupsNav";
import { Box } from "@mui/material";
import React, { useContext, useEffect } from "react";
import { useTheme } from "@mui/material/styles";
import ServersNav from "../components/ServersNav";
import Posts from "@/components/posts/Posts";
import Qna from "@/components/qna/Qna";
import Ask from "@/components/ask/Ask";
import { GlobalContext } from "./_app";
import { getFromStorage } from "@/helpers/localStorage";

export default function Home() {
  const theme = useTheme();

  const { global, setGlobal } = useContext(GlobalContext);

  useEffect(() => {
    if (!getFromStorage("token")) {
      window.location.href =
        window.location.origin + "/frontend/out/login.html";
    } else {
      setGlobal((prev) => {
        return { ...prev, loadingProgress: 0 };
      });
    }
  }, []);
  return (
    <>
      {getFromStorage("token") && (
        <Box display={"flex"} bgcolor={theme.palette.backgroundPrimary.lighter}>
          <Box width="72px">
            <ServersNav />
          </Box>
          <Box width="120px">
            <GroupsNav />
          </Box>
          <Box
            style={{ width: "100%", maxHeight: "100vh", overflow: "scroll" }}
          >
            <Posts />
            {/* <Qna /> */}
            {/* <Ask /> */}
          </Box>
        </Box>
      )}
    </>
  );
}
