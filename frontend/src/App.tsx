import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { refreshAccessToken, getAccessToken } from "./auth";
import { Tables } from "./features/Tables";
import { TableDetail } from "./features/TableDetail";
import { UserProvider } from "./contexts/UserContext";
import { Loader2 } from "lucide-react";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();

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
      
      if (!refreshed) {
        navigate("/login");
      }
    }

    checkAuth();
  }, [navigate]);

  if (loading) {
    return (
      <div className="min-h-screen game-gradient flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
          <div className="text-lg">Loading...</div>
          <div className="text-sm text-muted-foreground">Checking authentication</div>
        </div>
      </div>
    );
  }

  if (!loggedIn) {
    // This shouldn't happen as we navigate to /login, but as a fallback
    navigate("/login");
    return null;
  }

  // Render the appropriate component based on the current path
  if (location.pathname.startsWith("/tables/")) {
    return (
      <UserProvider>
        <TableDetail />
      </UserProvider>
    );
  } else if (location.pathname === "/tables") {
    return (
      <UserProvider>
        <Tables />
      </UserProvider>
    );
  } else {
    return (
      <UserProvider>
        <div className="min-h-screen game-gradient">
          <div className="max-w-7xl mx-auto p-6 space-y-6">
            <h1 className="text-3xl font-bold text-center mb-8">Card Game Arena</h1>
            <Tables />
          </div>
        </div>
      </UserProvider>
    );
  }
}
