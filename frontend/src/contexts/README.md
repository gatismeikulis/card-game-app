# User Context System

This directory contains the user context system that provides access to user information throughout the frontend application.

## Files

- `UserContext.tsx` - Main context provider and hooks
- `README.md` - This documentation file

## Usage

### 1. Basic Setup

The `UserProvider` is already integrated into the app in `App.tsx`. All components within the app have access to user data.

### 2. Available Hooks

#### `useUser()`

Returns the raw user context with loading states and error handling.

```typescript
import { useUser } from "../contexts/UserContext";

function MyComponent() {
  const { user, isLoading, error, refetch } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>No user data</div>;

  return <div>Welcome, {user.screen_name}!</div>;
}
```

#### `useUserData()`

Returns processed user data with convenient properties.

```typescript
import { useUserData } from "../contexts/UserContext";

function MyComponent() {
  const {
    user,
    isLoading,
    error,
    isLoggedIn,
    userId,
    username,
    email,
    screenName,
    description,
  } = useUserData();

  return <div>Hello, {screenName}!</div>;
}
```

#### `useGameDisplayName()` (from UserInfo.tsx)

Returns the best display name for game purposes (screen_name or username).

```typescript
import { useGameDisplayName } from "../components/UserInfo";

function GameComponent() {
  const displayName = useGameDisplayName();
  return <div>Player: {displayName}</div>;
}
```

### 3. User Data Structure

The user object contains the following fields from `/api/v1/users/me`:

```typescript
interface User {
  id: number;
  username: string;
  email: string;
  screen_name: string;
  description: string;
}
```

### 4. Examples

#### Display User Info

```typescript
import { useUserData } from "../contexts/UserContext";

function UserProfile() {
  const { user, isLoading } = useUserData();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <h2>{user?.screen_name}</h2>
      <p>Email: {user?.email}</p>
      <p>Description: {user?.description}</p>
    </div>
  );
}
```

#### Conditional Rendering Based on User

```typescript
import { useUserData } from "../contexts/UserContext";

function AdminPanel() {
  const { userId, isLoggedIn } = useUserData();

  if (!isLoggedIn) return <div>Please log in</div>;

  // Show admin content for specific users
  if (userId === 1) {
    return <div>Admin Panel</div>;
  }

  return <div>Regular User Panel</div>;
}
```

#### Game Display Names

```typescript
import { useGameDisplayName } from "../components/UserInfo";

function GamePlayer() {
  const displayName = useGameDisplayName();

  return <div>Current Player: {displayName}</div>;
}
```

### 5. Features

- **Automatic Caching**: User data is cached for 5 minutes
- **Error Handling**: Built-in error states and retry logic
- **Loading States**: Proper loading indicators
- **Type Safety**: Full TypeScript support
- **React Query Integration**: Uses React Query for data fetching and caching

### 6. API Integration

The context automatically fetches user data from `/api/v1/users/me` endpoint and handles:

- Authentication tokens
- Error responses
- Network failures
- Data refresh

### 7. Performance

- Data is cached for 5 minutes (`staleTime`)
- Garbage collection after 10 minutes (`gcTime`)
- Automatic refetch on window focus
- Retry logic for failed requests
