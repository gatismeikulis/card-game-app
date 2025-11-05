import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import { Register } from "./features/Register";
import { LoginForm } from "./auth";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginForm onLoggedIn={() => (window.location.href = "/")} />,
  },
  {
    path: "/register",
    element: <Register />,
  },
  { path: "/", element: <App /> },
  { path: "/tables", element: <App /> },
  { path: "/tables/:id", element: <App /> },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
