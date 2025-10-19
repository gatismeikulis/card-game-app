import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import { TableDetail } from "./features/TableDetail";
import { Tables } from "./features/Tables";

const router = createBrowserRouter([
  { path: "/", element: <App /> },
  { path: "/tables", element: <App /> },
  { path: "/tables/:id", element: <App /> },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
