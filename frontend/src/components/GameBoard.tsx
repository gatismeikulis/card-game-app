// GameBoard component for HTML-based game interface
import { Player } from "./Player";
import { PlayerHand } from "./PlayerHand";
import { PlayingCard } from "./PlayingCard";

// Helper to render suit as a colored badge with full name
const renderSuitBadge = (value: any) => {
  if (!value)
    return (
      <span className="px-2 py-0.5 rounded border text-sm text-gray-500">
        N/A
      </span>
    );
  const sym = String(value).trim().toLowerCase();
  const map: Record<string, { name: string; cls: string }> = {
    s: { name: "SPADE", cls: "bg-gray-100 text-black border-gray-300" },
    h: { name: "HEART", cls: "bg-red-100 text-red-700 border-red-300" },
    d: { name: "DIAMOND", cls: "bg-red-100 text-red-700 border-red-300" },
    c: { name: "CLUB", cls: "bg-gray-100 text-black border-gray-300" },
  };
  const info = map[sym] || {
    name: sym.toUpperCase(),
    cls: "bg-gray-100 text-black border-gray-300",
  };
  return (
    <span className={`px-2 py-0.5 rounded border text-sm ${info.cls}`}>
      {info.name}
    </span>
  );
};

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
  requiredSuit?: string;
  trumpSuit?: string;
  lastTrick?: string[];
  highestBid?: { bidder: string; amount: number };
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
  trumpSuit,
  lastTrick,
  highestBid,
  className = "",
}: GameBoardProps) {
  // Calculate player positions around the table
  const getPlayerPosition = (seatNumber: number) => {
    if (seatNumber === currentUserSeat) return "bottom";
    // for spectators view
    if(!currentUserSeat && seatNumber === 1) return "bottom";
    if(!currentUserSeat && seatNumber === 2) return "left";
    if(!currentUserSeat && seatNumber === 3) return "right";

    // for non current players
    if(currentUserSeat === 1 && seatNumber === 2) return "left";
    if(currentUserSeat === 1 && seatNumber === 3) return "right";
    if(currentUserSeat === 2 && seatNumber === 1) return "right";
    if(currentUserSeat === 2 && seatNumber === 3) return "left";
    if(currentUserSeat === 3 && seatNumber === 1) return "left";
    if(currentUserSeat === 3 && seatNumber === 2) return "right";

    // Default fallback
    return "top";
  };

  const otherPlayers = players.filter((p) => p.seat_number !== currentUserSeat);
  const currentUser = players.find((p) => p.seat_number === currentUserSeat);

  return (
    <div
      className={`relative w-full max-w-full h-[28rem] sm:h-[32rem] md:h-[36rem] lg:h-[40rem] xl:h-[44rem] bg-gradient-to-br from-green-800 to-green-900 rounded-lg border-2 border-green-700 overflow-hidden ${className}`}
    >
      {/* Game table background */}
      <div className="absolute inset-4 bg-green-600 rounded-full opacity-30 z-0"></div>

      {/* Top area for current player info */}
      <div className="absolute top-1 left-1/2 transform -translate-x-1/2 z-10 px-2">
        <div className="text-center">
          {phase && activeSeat && (
            <div className="text-xs sm:text-sm md:text-base text-white whitespace-nowrap">
              <span className="font-semibold">{phase}</span>
              {(() => {
                const activePlayer = players.find(
                  (p) => p.seat_number === activeSeat
                );
                return (
                  <span className="text-green-200 ml-2">
                    •{" "}
                    {(activePlayer as any)?.screen_name ||
                      activePlayer?.name ||
                      `Player ${activeSeat}`}
                    's turn
                  </span>
                );
              })()}
            </div>
          )}
          {!activeSeat && (
            <div className="text-xs sm:text-sm md:text-base font-semibold text-white">
              {phase || "Game in Progress"}
            </div>
          )}
        </div>
      </div>

      {/* Mobile Game Info - Top Left Corner */}
      {phase === "Playing Cards" && (
        <div className="absolute top-8 left-2 z-10 lg:hidden">
          <div className="bg-black/20 rounded-lg p-2 text-white text-xs">
          <div className="font-semibold mb-1">TRUMP</div>
           
                  {renderSuitBadge(trumpSuit)}

          </div>
        </div>
      )}

      {/* Mobile Last Trick - Right Bottom */}
      {lastTrick && lastTrick.length > 0 && (
        <div className="absolute bottom-32 right-2 z-10 lg:hidden">
          <div className="bg-black/20 rounded-lg p-2 text-white text-xs">
            <h4 className="text-sm font-semibold text-primary mb-2">
              Last Trick
            </h4>
            <div className="flex flex-wrap gap-1">
              {lastTrick.map((card, idx) => {
                const cardStr = String(card);
                const suit = cardStr.slice(-1);
                let cardColor = "bg-background text-foreground border";

                if (suit === "h" || suit === "d") {
                  cardColor = "bg-red-100 text-red-800 border-red-300";
                } else if (suit === "s" || suit === "c") {
                  cardColor = "bg-gray-100 text-gray-800 border-gray-300";
                }

                return (
                  <span
                    key={idx}
                    className={`text-sm px-2 py-1 rounded border font-bold ${cardColor}`}
                  >
                    {cardStr}
                  </span>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Mobile Highest Bid - Right Side */}
      {highestBid && (
        <div className="absolute top-8 right-2 z-10 lg:hidden">
          <div className="bg-black/20 rounded-lg p-2 text-white text-xs">
            <div className="font-semibold mb-1">HIGHEST BIDDER</div>
            <div>
              <span className="text-green-300">{highestBid.bidder}:</span>
              <span className="ml-1 font-mono">{highestBid.amount}</span>
            </div>
          </div>
        </div>
      )}

      {/* Center area for cards on board and bidding panel */}
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <div className="text-center">
          {/* Bidding Panel */}
          {biddingPanel && (
            <div className="mb-24 pt-2">{biddingPanel}</div>
          )}

          {/* Cards on board during playing phase */}
          {phase === "Playing Cards" &&
            Object.keys(cardsOnBoard).length > 0 && (
              <div className="flex justify-center gap-2 mt-2 sm:mt-4">
                {Object.entries(cardsOnBoard).map(([seat, card]) => {
                  if (!card) return null;
                  return (
                    <div key={seat} className="text-center mb-24 sm:mb-2">
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
        const position = getPlayerPosition(player.seat_number);
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
          {playerStats && phase === "Playing Cards" && (
            <div className="absolute left-0 bottom-32 bg-black/20 rounded-lg p-1 sm:p-2 text-white text-xs">
              {playerStats.points !== undefined && (
                <div className="flex justify-between">
                  <span className="text-green-300 font-bold text-sm">
                    POINTS:
                  </span>
                  <span className="font-mono text-sm font-bold">
                    {playerStats.points}
                  </span>
                </div>
              )}
              {playerStats.trick_count !== undefined && (
                <div className="flex justify-between">
                  <span className="text-blue-300 font-bold text-sm">
                    TRICKS:
                  </span>
                  <span className="font-mono text-sm font-bold">
                    {playerStats.trick_count}
                  </span>
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
