import { createBrowserRouter } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import AuthTestPage from "./pages/AuthTestPage";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: LandingPage,
  },
  {
    path: "/login",
    Component: LoginPage,
  },
  {
    path: "/dashboard",
    Component: Dashboard,
  },
  {
    path: "/auth-test",
    Component: AuthTestPage,
  },
]);