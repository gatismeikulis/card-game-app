import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { refreshAccessToken, getAccessToken } from "./auth";
import { Tables } from "./features/Tables";
import { TableDetail } from "./features/TableDetail";
import { UserProvider } from "./contexts/UserContext";
import { Loader2 } from "lucide-react";

export default function App() {
  const [loading, setLoading] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    async function checkAuth() {
      // If we already have an access token in memory, we're logged in
      const existingToken = getAccessToken();

      if (existingToken) {
        setLoading(false);
        return;
      }

      // Try to refresh the token
      const refreshed = await refreshAccessToken();
      setLoading(false);

      // Don't redirect to login - allow viewing tables without authentication
      // Only redirect to login for routes that require authentication
      const publicRoutes = ["/", "/tables", "/tables/"];
      const isPublicRoute = publicRoutes.some((route) =>
        location.pathname === route || location.pathname.startsWith("/tables/")
      );

      if (!refreshed && !isPublicRoute) {
        navigate("/login");
      }
    }

    checkAuth();
  }, [navigate, location.pathname]);

  if (loading) {
    return (
      <div className="min-h-screen game-gradient flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
          <div className="text-lg">Loading...</div>
          <div className="text-sm text-muted-foreground">
            Checking authentication
          </div>
        </div>
      </div>
    );
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
            <h1 className="text-3xl font-bold text-center mb-8">
              Card Game Arena
            </h1>
            <Tables />
          </div>
        </div>
      </UserProvider>
    );
  }
}
