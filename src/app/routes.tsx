import { createBrowserRouter } from "react-router";
import LoginPage from "./pages/LoginPage";
import DashboardLayout from "./components/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import DataPage from "./pages/DataPage";
import AdminPanel from "./pages/AdminPanel";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPage />,
  },
  {
    path: "/",
    element: <DashboardLayout />,
    children: [
      {
        path: "dashboard",
        element: <Dashboard />,
      },
      {
        path: "data",
        element: <DataPage />,
      },
      {
        path: "admin",
        element: <AdminPanel />,
      },
    ],
  },
]);
