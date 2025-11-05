import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from "react";
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api";
import { getAccessToken } from "../auth";

// User data interface
export interface User {
  id: number;
  username: string;
  email: string;
  screen_name: string;
  description: string;
}

// Context interface
interface UserContextType {
  user: User | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => void;
}

// Create context
const UserContext = createContext<UserContextType | undefined>(undefined);

// Provider component
interface UserProviderProps {
  children: ReactNode;
}

export function UserProvider({ children }: UserProviderProps) {
  const [user, setUser] = useState<User | null>(null);

  // Fetch user data - allow this to fail gracefully if not authenticated
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["user", "me"],
    queryFn: async () => {
      const response = await apiFetch("/api/v1/users/me/");
      return response;
    },
    retry: false, // Don't retry if not authenticated
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
    // Only run query if we have a token
    enabled: !!getAccessToken(),
  });

  // Update user state when data changes
  useEffect(() => {
    if (data) {
      setUser(data);
    }
  }, [data]);

  const contextValue: UserContextType = {
    user,
    isLoading,
    error: error as Error | null,
    refetch,
  };

  return (
    <UserContext.Provider value={contextValue}>{children}</UserContext.Provider>
  );
}

// Hook to use user context
export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
}

// Hook to get user data with loading state
export function useUserData() {
  const { user, isLoading, error } = useUser();

  return {
    user,
    isLoading,
    error,
    isLoggedIn: !!user,
    userId: user?.id,
    username: user?.username,
    email: user?.email,
    screenName: user?.screen_name,
    description: user?.description,
  };
}
