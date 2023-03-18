import React, { useEffect } from "react";
import DeleteForeverOutlinedIcon from "@mui/icons-material/DeleteForeverOutlined";
import { useState } from "react";
import { useTheme } from "@mui/material/styles";
import useSWR from "swr";
import { Button, CircularProgress, Typography } from "@mui/material";
import { GlobalContext } from "@/pages/_app";
import nextConfig from "@/next.config";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function Groups() {
  const { data, error } = useSWR("http://127.0.0.1:8000/get-all-apps", fetcher);
  const [tab, setTab] = useState();
  const theme = useTheme();
  const handleTab = (e, value) => {
    let url = window.location.origin + "/" + value;
    if (url != window.location.href) {
      window.location.href = url;
    }
  };
  useEffect(() => {
    if (data) {
      let filteredData = data.filter((item) =>
          window.location.href.includes(item)
        );
        if (filteredData) setTab(filteredData[0]);
    }
  }, [data]);
  return (
    <>
      {!data ? (
        <CircularProgress />
      ) : (
        data.map((application) => (
          <Button
            key={application.app}
            width="100%"
            onClick={(e) => handleTab(e, application.app)}
            endIcon={<DeleteForeverOutlinedIcon color="error" />}
            style={{
              justifyContent: "space-between",
              borderRadius: "0",
              backgroundColor:
                tab === application.app
                  ? theme.palette.backgroundPrimary.main
                  : "#FFFFFF",
            }}
          >
            <Typography
              fontSize="12px"
              lineHeight="20px"
              fontFamily={"Inter"}
              fontWeight={500}
              color={theme.palette.textColor.main}
            >
              {application.app}
            </Typography>
          </Button>
        ))
      )}
    </>
  );
}
