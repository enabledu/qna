import { Stack } from "@mui/system";
import React from "react";
import { Button, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import Groups from "./Groups";

const GroupsNav = () => {
  const theme = useTheme();

  return (
    <Stack height="100vh" backgroundColor={"#FFFFFF"} paddingY="16px">
      <Groups />
      <Button width="100%" style={{ justifyContent: "start" }}>
        <Typography
          fontSize="12px"
          lineHeight="20px"
          fontFamily={"Inter"}
          fontWeight={500}
          color={theme.palette.primary.main}
        >
          + Add
        </Typography>
      </Button>
    </Stack>
  );
};

export default GroupsNav;
