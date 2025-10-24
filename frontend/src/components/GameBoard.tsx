// GameBoard component for HTML-based game interface
import { Player } from "./Player";
import { PlayerHand } from "./PlayerHand";
import { PlayingCard } from "./PlayingCard";

interface GameBoardProps {
  players: Array<{
    name: string;
    seat_number: number;
    hand_size?: number;
    tricks_taken?: number;
    bid?: number;
  }>;
  currentUserSeat?: number;
  currentUserHand?: string[];
  selectedCards: string[];
  hoveredCard: string | null;
  onCardClick: (card: string) => void;
  onCardHover: (card: string | null) => void;
  activeSeat?: number;
  phase?: string;
  cardsOnBoard?: Record<string, string | null>;
  biddingPanel?: React.ReactNode;
  playerStats?: {
    points?: number;
    marriage_points?: string[];
    trick_count?: number;
  };
  className?: string;
}

export function GameBoard({
  players,
  currentUserSeat,
  currentUserHand = [],
  selectedCards,
  hoveredCard,
  onCardClick,
  onCardHover,
  activeSeat,
  phase,
  cardsOnBoard = {},
  biddingPanel,
  playerStats,
  className = "",
}: GameBoardProps) {
  // Calculate player positions around the table
  const getPlayerPosition = (seatNumber: number, totalPlayers: number) => {
    if (totalPlayers === 3) {
      // For 3 players: current user at bottom (6 o'clock), others at 10 and 2 o'clock
      if (seatNumber === currentUserSeat) return "bottom";
      // Position other players at 10 o'clock and 2 o'clock
      const otherSeats = players.filter(
        (p) => p.seat_number !== currentUserSeat
      );
      if (otherSeats.length >= 1 && seatNumber === otherSeats[0].seat_number)
        return "left";
      if (otherSeats.length >= 2 && seatNumber === otherSeats[1].seat_number)
        return "right";
    }
    // Default fallback
    return "top";
  };

  const otherPlayers = players.filter((p) => p.seat_number !== currentUserSeat);
  const currentUser = players.find((p) => p.seat_number === currentUserSeat);

  return (
    <div
      className={`relative w-full max-w-full h-80 sm:h-96 md:h-[28rem] lg:h-[32rem] xl:h-[36rem] bg-gradient-to-br from-green-800 to-green-900 rounded-lg border-2 border-green-700 overflow-hidden ${className}`}
    >
      {/* Game table background */}
      <div className="absolute inset-4 bg-green-600 rounded-full opacity-30 z-0"></div>

      {/* Top area for current player info */}
      <div className="absolute top-2 left-1/2 transform -translate-x-1/2 z-10">
        <div className="text-center">
          <div className="text-lg font-semibold text-white">
            {phase || "Game in Progress"}
          </div>
          {activeSeat &&
            (() => {
              const activePlayer = players.find(
                (p) => p.seat_number === activeSeat
              );
              return (
                <div className="text-sm text-green-200 mt-1">
                  {(activePlayer as any)?.screen_name ||
                    activePlayer?.name ||
                    `Player ${activeSeat}`}
                  's turn
                </div>
              );
            })()}
        </div>
      </div>

      {/* Center area for cards on board and bidding panel */}
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <div className="text-center">
          {/* Bidding Panel */}
          {biddingPanel && <div className="mb-2 -mt-8">{biddingPanel}</div>}

          {/* Cards on board during playing phase */}
          {phase === "Playing Cards" &&
            Object.keys(cardsOnBoard).length > 0 && (
              <div className="flex justify-center gap-2 mt-4">
                {Object.entries(cardsOnBoard).map(([seat, card]) => {
                  if (!card) return null;
                  return (
                    <div key={seat} className="text-center">
                      <div className="text-xs text-green-200 mb-1">
                        {(() => {
                          const player = players.find(
                            (p) => p.seat_number === parseInt(seat)
                          );
                          return (
                            (player as any)?.screen_name ||
                            player?.name ||
                            `Seat ${seat}`
                          );
                        })()}
                      </div>
                      <PlayingCard
                        card={card}
                        size="lg"
                        className="shadow-md"
                      />
                    </div>
                  );
                })}
              </div>
            )}
        </div>
      </div>

      {/* Other players positioned around the table */}
      {otherPlayers.map((player) => {
        const position = getPlayerPosition(player.seat_number, players.length);
        return (
          <Player
            key={player.seat_number}
            name={(player as any).screen_name || player.name}
            seatNumber={player.seat_number}
            handSize={player.hand_size}
            tricksTaken={player.tricks_taken}
            bid={player.bid}
            isActive={activeSeat === player.seat_number}
            position={position as "top" | "left" | "right" | "bottom"}
            phase={phase}
            className="z-10"
          />
        );
      })}

      {/* Current user's hand at the bottom */}
      {currentUser && currentUserHand.length > 0 && (
        <div className="absolute bottom-2 sm:bottom-4 left-1/2 transform -translate-x-1/2 w-full max-w-full px-2 sm:px-4 z-50">
          {/* Player Stats - Left side */}
          {playerStats && (
            <div className="absolute left-0 top-0 bg-black/20 rounded-lg p-1 sm:p-2 text-white text-xs">
              <div className="font-semibold mb-1">Your Stats</div>
              {playerStats.points !== undefined && (
                <div className="flex justify-between">
                  <span className="text-green-300">Points:</span>
                  <span className="font-mono">{playerStats.points}</span>
                </div>
              )}
              {playerStats.trick_count !== undefined && (
                <div className="flex justify-between">
                  <span className="text-blue-300">Tricks:</span>
                  <span className="font-mono">{playerStats.trick_count}</span>
                </div>
              )}
            </div>
          )}

          <PlayerHand
            cards={currentUserHand}
            selectedCards={selectedCards}
            hoveredCard={hoveredCard}
            onCardClick={onCardClick}
            onCardHover={onCardHover}
            className="overflow-x-auto"
          />
        </div>
      )}
    </div>
  );
}
