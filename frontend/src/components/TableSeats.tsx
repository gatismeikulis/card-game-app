import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

interface TableSeatsProps {
  players: any[];
  userId: number | undefined;
  maxPlayers: number;
  onJoin: (seatNumber: number) => void;
  onJoinAny: () => void;
  onLeave: () => void;
  onAddBot: (seatNumber: number) => void;
  onRemoveBot: (seatNumber: number) => void;
  isPending: boolean;
  isAuthenticated: boolean;
}

export function TableSeats({
  players,
  userId,
  maxPlayers,
  onJoin,
  onJoinAny,
  onLeave,
  onAddBot,
  onRemoveBot,
  isPending,
  isAuthenticated,
}: TableSeatsProps) {
  const seatNumbers = [1, 2, 3];
  const canJoinAny =
    players.length < maxPlayers &&
    !players.some((p: any) => p.user_id === userId);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Table Seats</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {seatNumbers.map((seatNum) => {
            const player = players?.find(
              (p: any) => p.seat_number === seatNum
            );
            const isSeatTaken = !!player;
            const isCurrentUser =
              player && !player.bot_strategy_kind && player.user_id === userId;
            const isBot = player && player.bot_strategy_kind;
            const canJoin =
              !isSeatTaken &&
              players.length < maxPlayers &&
              !players.some((p: any) => p.user_id === userId);

            return (
              <Card key={seatNum} className="card-hover">
                <CardContent className="pt-6 text-center">
                  <div className="text-sm text-muted-foreground mb-3">
                    Seat {seatNum}
                  </div>
                  {isSeatTaken ? (
                    <div className="space-y-3">
                      <div className="font-medium text-lg">
                        {player.screen_name}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {isBot
                          ? `Bot (${player.bot_strategy_kind})`
                          : "Human Player"}
                      </div>
                      {isBot && (
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => onRemoveBot(seatNum)}
                          disabled={isPending}
                          className="w-full"
                        >
                          {isPending ? "Removing..." : "Remove Bot"}
                        </Button>
                      )}
                      {isCurrentUser && (
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={onLeave}
                          disabled={isPending}
                          className="w-full"
                        >
                          {isPending ? "Leaving..." : "Leave Table"}
                        </Button>
                      )}
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <div className="text-muted-foreground text-sm mb-3">
                        Empty Seat
                      </div>
                            <div className="flex flex-col gap-2">
                              {isAuthenticated ? (
                                <>
                                  <Button
                                    size="sm"
                                    onClick={() => onJoin(seatNum)}
                                    disabled={isPending || !canJoin}
                                    className="w-full"
                                  >
                                    {isPending ? "Joining..." : "Join Table"}
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="secondary"
                                    onClick={() => onAddBot(seatNum)}
                                    disabled={isPending}
                                    className="w-full"
                                  >
                                    {isPending ? "Adding..." : "Add Bot"}
                                  </Button>
                                </>
                              ) : (
                                <div className="text-sm text-muted-foreground text-center py-2">
                                  Login to join
                                </div>
                              )}
                            </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

