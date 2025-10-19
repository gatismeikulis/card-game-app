import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { LoginForm, refreshAccessToken, getAccessToken } from "./auth";
import { Tables } from "./features/Tables";
import { TableDetail } from "./features/TableDetail";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    async function checkAuth() {
      // If we already have an access token in memory, we're logged in
      const existingToken = getAccessToken();

      if (existingToken) {
        setLoggedIn(true);
        setLoading(false);
        return;
      }

      // Try to refresh the token
      const refreshed = await refreshAccessToken();
      setLoggedIn(refreshed);
      setLoading(false);
    }

    checkAuth();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 text-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg">Loading...</div>
          <div className="text-sm text-gray-600">Checking authentication</div>
        </div>
      </div>
    );
  }

  if (!loggedIn) {
    return (
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <div className="max-w-2xl mx-auto p-6 space-y-6">
          <h1 className="text-2xl font-semibold">Card Game Client</h1>
          <LoginForm onLoggedIn={() => setLoggedIn(true)} />
        </div>
      </div>
    );
  }

  // Render the appropriate component based on the current path
  if (location.pathname.startsWith("/tables/")) {
    return <TableDetail />;
  } else if (location.pathname === "/tables") {
    return <Tables />;
  } else {
    return (
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <div className="max-w-2xl mx-auto p-6 space-y-6">
          <h1 className="text-2xl font-semibold">Card Game Client</h1>
          <Tables />
        </div>
      </div>
    );
  }
}
