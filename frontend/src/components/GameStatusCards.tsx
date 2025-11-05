import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { safeRender } from "../utils/gameUtils";

interface GameStatusCardsProps {
  status: string;
  roundNumber: any;
  summary: Record<string, number> | undefined;
  players: any[];
}

export function GameStatusCards({
  status,
  roundNumber,
  summary,
  players,
}: GameStatusCardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Status</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg font-semibold">{status}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Round</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg font-semibold">{safeRender(roundNumber)}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Scores</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm space-y-1">
            {summary
              ? Object.entries(summary).map(([seat, points]) => {
                  const player = players?.find(
                    (p: any) => p.seat_number === parseInt(seat)
                  );
                  const playerName = player?.screen_name || `Seat ${seat}`;
                  return (
                    <div key={seat} className="flex justify-between">
                      <span>{playerName}:</span>
                      <span className="font-semibold">{String(points)}</span>
                    </div>
                  );
                })
              : "No scores yet"}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

