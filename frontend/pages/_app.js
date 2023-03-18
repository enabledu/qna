"use client";

import * as React from "react";
import Head from "next/head";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { CacheProvider } from "@emotion/react";
import theme from "../config/theme";
import createEmotionCache from "../config/createEmotionCache";
import { Alert, LinearProgress } from "@mui/material";

// Client-side cache, shared for the whole session of the user in the browser.
const clientSideEmotionCache = createEmotionCache();
export const GlobalContext = React.createContext();

export default function MyApp(props) {
  const { Component, emotionCache = clientSideEmotionCache, pageProps } = props;
  const [global, setGlobal] = React.useState({
    loadingProgress: 0,
    user: null,
    alert: { title: null, severity: null },
  });

  return (
    <CacheProvider value={emotionCache}>
      <Head>
        <meta name="viewport" content="initial-scale=1, width=device-width" />
      </Head>
      <ThemeProvider theme={theme}>
        <GlobalContext.Provider value={{ global, setGlobal }}>
          {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
          <CssBaseline />
          {global.alert.title ? (
            <Alert
              severity={global.alert.severity}
              onClose={() => {
                setGlobal((prev) => {
                  return { ...prev, alert: {} };
                });
              }}
            >
              {global.alert.title}
            </Alert>
          ) : (
            ""
          )}
          {global.loadingProgress ? (
            <LinearProgress
              variant="determinate"
              color="primary"
              value={global.loadingProgress}
            />
          ) : (
            ""
          )}
          <Component {...pageProps} />
        </GlobalContext.Provider>
      </ThemeProvider>
    </CacheProvider>
  );
}
