import { Box, Stack } from "@mui/system";
import ToggleButton from "@mui/material/ToggleButton";
import React from "react";
import { ToggleButtonGroup } from "@mui/material";
import ApartmentIcon from "@mui/icons-material/Apartment";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import { useTheme } from "@mui/material/styles";
import AccountCircleOutlinedIcon from "@mui/icons-material/AccountCircleOutlined";
import AppinsIcon from "./icons/AppinsIcon";

const ServersNav = () => {
  const [tab, setTab] = useState("default");
  const theme = useTheme();

  const handleTab = (event, newTab) => {
    setTab(newTab);
  };

  return (
    <Stack
      height="100vh"
      justifyContent="space-between"
      backgroundColor={theme.palette.primary.main}
      padding="16px"
    >
      <Box
        display="flex"
        flexDirection={"column"}
        alignItems="center"
        gap={"16px"}
      >
        <Link href="/">
          <AppinsIcon />
        </Link>
        <ToggleButtonGroup
          color="black"
          value={tab}
          exclusive
          onChange={handleTab}
        >
          <ToggleButton style={{ border: "none" }} value="default">
            <ApartmentIcon width={16} color="secondary" />
          </ToggleButton>
        </ToggleButtonGroup>
      </Box>
      <Box display={"flex"} justifyContent="center" alignItems="center">
        <Link href="/">
          <AccountCircleOutlinedIcon
            width="24px"
            height="24px"
            color="secondary"
          />
        </Link>
      </Box>
    </Stack>
  );
};

export default ServersNav;
