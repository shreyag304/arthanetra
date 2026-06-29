import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "../pages/Login";
import Workspace from "../pages/Workspace";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Default Route */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Login */}
        <Route path="/login" element={<Login />} />

        {/* AI Workspace */}
        <Route path="/workspace" element={<Workspace />} />

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;