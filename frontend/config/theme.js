import { createTheme } from "@mui/material/styles";
import { red } from "@mui/material/colors";
// Create a theme instance.
const theme = createTheme({
  palette: {
    primary: {
      main: "#5048E5",
    },
    secondary: {
      main: "#FFFFFF",
    },
    black: {
      main: "#000000",
    },
    textColor: {
      main: "#374151",
    },
    backgroundPrimary: {
      main: "#F3F4F6",
      lighter: "#F9FAFB",
    },
    error: {
      main: red.A400,
    },
  },
});
export default theme;
