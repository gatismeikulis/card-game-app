import { Button } from "./ui/button";
import { LogOut, Play, LogIn } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface TableHeaderProps {
  wsConnected: boolean;
  hasGameState: boolean;
  canJoin: boolean;
  canStartGame: boolean;
  onJoin: () => void;
  onStartGame: () => void;
  onBack: () => void;
  isPending: boolean;
  isAuthenticated: boolean;
}

export function TableHeader({
  wsConnected,
  hasGameState,
  canJoin,
  canStartGame,
  onJoin,
  onStartGame,
  onBack,
  isPending,
  isAuthenticated,
}: TableHeaderProps) {
  const navigate = useNavigate();

  return (
    <div className="flex flex-wrap items-center justify-between gap-4">
      <div className="flex gap-2">
        <div
          className={`px-3 py-1.5 rounded text-sm font-medium ${
            wsConnected
              ? "bg-green-500/20 text-green-600"
              : "bg-yellow-500/20 text-yellow-600"
          }`}
        >
          {wsConnected ? "● Connected" : "○ Disconnected"}
        </div>
        {!isAuthenticated && (
          <div className="px-3 py-1.5 rounded text-sm font-medium bg-blue-500/20 text-blue-600">
            View Only (Not Logged In)
          </div>
        )}
      </div>
      <div className="flex gap-2">
        {!isAuthenticated ? (
          <Button
            size="sm"
            variant="default"
            onClick={() => navigate("/login")}
          >
            <LogIn className="mr-2 h-4 w-4" />
            Login to Join
          </Button>
        ) : (
          <>
            {!hasGameState && (
              <>
                <Button size="sm" onClick={onJoin} disabled={!canJoin || isPending}>
                  Join Table
                </Button>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={onStartGame}
                  disabled={!canStartGame || isPending}
                >
                  <Play className="mr-2 h-4 w-4" />
                  Start Game
                </Button>
              </>
            )}
          </>
        )}
        <Button size="sm" variant="outline" onClick={onBack}>
          <LogOut className="mr-2 h-4 w-4" />
          Return
        </Button>
      </div>
    </div>
  );
}

