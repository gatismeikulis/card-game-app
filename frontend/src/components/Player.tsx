import type { ReactNode } from "react";
import { HiddenCard } from "./HiddenCard";

interface PlayerProps {
  name: string;
  seatNumber: number;
  handSize?: number;
  tricksTaken?: number;
  bid?: number;
  isCurrentUser?: boolean;
  isActive?: boolean;
  position: "top" | "left" | "right" | "bottom";
  phase?: string;
  className?: string;
  action?: ReactNode;
}

export function Player({
  name,
  handSize,
  tricksTaken,
  bid,
  isCurrentUser = false,
  isActive = false,
  position,
  phase,
  className = "",
  action,
}: PlayerProps) {
  const positionClasses = {
    top: "top-1 sm:top-2 left-1/2 transform -translate-x-1/2",
    left: "left-1 sm:left-2 top-1/3 transform -translate-y-1/2",
    right: "right-1 sm:right-2 top-1/3 transform -translate-y-1/2",
    bottom: "bottom-1 sm:bottom-2 left-1/2 transform -translate-x-1/2",
  };

  return (
    <div className={`absolute ${positionClasses[position]} ${className}`}>
      <div
        className={`
        relative bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg shadow-lg p-0.5 sm:p-1 md:p-2 min-w-[50px] sm:min-w-[60px] md:min-w-[80px] text-center border border-gray-600
        ${
          isActive
            ? "ring-2 ring-yellow-400 bg-gradient-to-br from-yellow-600 to-yellow-700"
            : ""
        }
        ${isCurrentUser ? "bg-gradient-to-br from-blue-600 to-blue-700" : ""}
      `}
      >
        <div className="font-semibold text-[10px] sm:text-xs md:text-sm text-white truncate px-1">
          {name}
        </div>
        {phase === "Bidding" ? (
          <div className="text-[9px] sm:text-xs text-green-300 mt-0.5 sm:mt-1 px-1">
            {bid !== undefined
              ? bid > 0
                ? `Bid: ${bid}`
                : bid < 0
                ? "PASSED"
                : "NOT BID YET"
              : "NOT BID YET"}
          </div>
        ) : (
          tricksTaken !== undefined && (
            <div className="text-[9px] sm:text-xs text-green-300 mt-0.5 sm:mt-1">
              {tricksTaken} tricks
            </div>
          )
        )}

        {/* Show hidden cards for other players - but NOT during bidding phase */}
        {!isCurrentUser && handSize && handSize > 0 && phase !== "Bidding" && (
          <div className="flex justify-center gap-0 mt-0.5 sm:mt-1">
            {Array.from({ length: Math.min(handSize, 10) }).map((_, index) => (
              <HiddenCard key={index} size="sm" className="-ml-1 first:ml-0" />
            ))}
          </div>
        )}
        {action && (
          <div className="absolute -top-2 -right-2">
            {action}
          </div>
        )}
      </div>
    </div>
  );
}
