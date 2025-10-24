import { useUserData } from "../contexts/UserContext";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Loader2, User } from "lucide-react";

export function UserInfo() {
  const { user, isLoading, error, screenName, username, email } = useUserData();

  if (isLoading) {
    return (
      <Card className="w-full max-w-sm">
        <CardContent className="p-4">
          <div className="flex items-center space-x-2">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span className="text-sm">Loading user info...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full max-w-sm border-destructive">
        <CardContent className="p-4">
          <div className="text-sm text-destructive">
            Error loading user info: {error.message}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!user) {
    return (
      <Card className="w-full max-w-sm">
        <CardContent className="p-4">
          <div className="text-sm text-muted-foreground">
            No user data available
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-sm">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg flex items-center space-x-2">
          <User className="h-5 w-5" />
          <span>User Info</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex justify-between">
          <span className="text-sm font-medium text-muted-foreground">ID:</span>
          <span className="text-sm font-mono">{user.id}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm font-medium text-muted-foreground">
            Username:
          </span>
          <span className="text-sm">{username}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm font-medium text-muted-foreground">
            Screen Name:
          </span>
          <span className="text-sm font-semibold text-primary">
            {screenName}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm font-medium text-muted-foreground">
            Email:
          </span>
          <span className="text-sm">{email}</span>
        </div>
        {user.description && (
          <div className="pt-2 border-t">
            <div className="text-sm font-medium text-muted-foreground mb-1">
              Description:
            </div>
            <div className="text-sm">{user.description}</div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Simple hook usage example
export function useUserDisplayName() {
  const { screenName, username } = useUserData();
  return screenName || username || "Unknown User";
}

// Hook to get user's display name for game purposes
export function useGameDisplayName() {
  const { screenName, username } = useUserData();
  return screenName || username || "Player";
}
