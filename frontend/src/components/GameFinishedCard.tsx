import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Play } from "lucide-react";

interface GameFinishedCardProps {
  gameState: any;
  players: any[];
  onStartNewGame: () => void;
  onBackToTables: () => void;
  isPending: boolean;
}

export function GameFinishedCard({
  gameState,
  players,
  onStartNewGame,
  onBackToTables,
  isPending,
}: GameFinishedCardProps) {
  const summary = gameState?.summary;
  if (!summary) return null;

  const sortedEntries = Object.entries(summary).sort(
    ([, a]: any, [, b]: any) => (b as number) - (a as number)
  );

  const allScores = Object.values(summary) as number[];
  const maxScore = Math.max(...allScores);

  return (
    <Card className="border-amber-500/50 bg-amber-500/10 card-glow">
      <CardHeader>
        <CardTitle className="text-2xl text-amber-500 flex items-center gap-2">
          🏆 Game Finished!
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h3 className="font-semibold mb-2">Final Scores:</h3>
          <div className="space-y-2">
            {sortedEntries.map(([seat, points]: [string, any]) => {
              const player = players?.find(
                (p: any) => p.seat_number === parseInt(seat)
              );
              const playerName = player?.screen_name || `Seat ${seat}`;
              const isWinner = points === maxScore;

              return (
                <div
                  key={seat}
                  className={`flex justify-between items-center p-2 rounded ${
                    isWinner
                      ? "bg-amber-500/20 border border-amber-500/50"
                      : "bg-muted/50"
                  }`}
                >
                  <span
                    className={`font-medium ${isWinner ? "text-amber-500" : ""}`}
                  >
                    {isWinner && "👑 "}
                    {playerName}
                  </span>
                  <span
                    className={`font-bold text-lg ${isWinner ? "text-amber-500" : ""}`}
                  >
                    {String(points)}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
        <div className="flex gap-2">
          <Button className="flex-1" onClick={onStartNewGame} disabled={isPending}>
            <Play className="mr-2 h-4 w-4" />
            {isPending ? "Starting..." : "Start New Game"}
          </Button>
          <Button variant="outline" onClick={onBackToTables}>
            Back to Tables
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

