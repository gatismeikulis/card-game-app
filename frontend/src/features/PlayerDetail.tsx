import type { FC } from "react";

interface PlayerDetailProps {
  bid: number;
  hand: string[] | number;
  marriage_points?: number[] | null;
  points: number;
  trick_count: number;
  screen_name: string;
  onCardClick?: (card: string) => void;
  isMyTurn?: boolean;
}

const formatPoints = (points: number, marriage_points?: number[] | null) => {
  if (!marriage_points || marriage_points.length === 0) {
    return points;
  }
  const marriageSum = marriage_points.reduce((a, b) => a + b, 0);
  if (marriageSum > 0) {
    return `${points} (${marriage_points.join(" + ")})`;
  }
  return points;
};

const getCardStyle = (card: string) => {
  if (!card || card.length < 2) return "bg-gray-100 text-gray-600";

  const suit = card.slice(-1); // Last character is suit
  switch (suit) {
    case "s":
      return "bg-gray-100 text-black border-gray-300"; // spades - light gray background
    case "h":
      return "bg-red-100 text-red-800 border-red-300"; // hearts - light red background
    case "d":
      return "bg-blue-100 text-blue-800 border-blue-300"; // diamonds - light blue background
    case "c":
      return "bg-green-100 text-green-800 border-green-300"; // clubs - light green background
    default:
      return "bg-gray-100 text-gray-600";
  }
};

export const PlayerDetail: FC<PlayerDetailProps> = ({
  bid,
  hand,
  marriage_points,
  points,
  trick_count,
  screen_name,
  onCardClick,
  isMyTurn = false,
}) => {
  return (
    <div className="bg-white border rounded-lg p-3 flex items-center gap-4">
      {/* Player Info Block */}
      <div className="min-w-0 flex-shrink-0">
        <h3 className="font-semibold text-sm">{screen_name}</h3>
        <div className="text-xs text-gray-600">
          {bid >= 0 ? `Bid: ${bid}` : "PASSED"}
        </div>
      </div>

      {/* Stats Block */}
      <div className="flex gap-3">
        <div className="bg-gray-50 rounded px-2 py-1 text-center min-w-0">
          <div className="text-xs text-gray-600">Points</div>
          <div className="font-semibold text-sm">
            {formatPoints(points, marriage_points)}
          </div>
        </div>
        <div className="bg-gray-50 rounded px-2 py-1 text-center min-w-0">
          <div className="text-xs text-gray-600">Tricks</div>
          <div className="font-semibold text-sm">{trick_count}</div>
        </div>
      </div>

      {/* Hand Block */}
      <div className="flex-1 min-w-0">
        <div className="text-xs text-gray-600 mb-1">
          Hand ({Array.isArray(hand) ? hand.length : hand} cards)
        </div>
        <div className="flex flex-wrap gap-1">
          {Array.isArray(hand)
            ? hand.map((card, i) => (
                <button
                  key={i}
                  className={`w-6 h-8 border rounded flex items-center justify-center text-xs transition-colors ${getCardStyle(
                    card,
                  )} ${
                    isMyTurn && onCardClick
                      ? "hover:shadow-md hover:scale-105 cursor-pointer"
                      : "cursor-not-allowed opacity-60"
                  }`}
                  onClick={() => {
                    if (isMyTurn && onCardClick) {
                      onCardClick(card);
                    }
                  }}
                  disabled={!isMyTurn || !onCardClick}
                >
                  {card}
                </button>
              ))
            : [...Array(hand)].map((_, i) => (
                <div key={i} className="w-6 h-8 border rounded bg-gray-100" />
              ))}
        </div>
      </div>
    </div>
  );
};
