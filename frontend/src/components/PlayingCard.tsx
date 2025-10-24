interface PlayingCardProps {
  card: string;
  isSelected?: boolean;
  isHovered?: boolean;
  onClick?: () => void;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
  className?: string;
  size?: "sm" | "md" | "lg";
}

export function PlayingCard({
  card,
  isSelected = false,
  isHovered = false,
  onClick,
  onMouseEnter,
  onMouseLeave,
  className = "",
  size = "md",
}: PlayingCardProps) {
  const suit = card.slice(-1);
  const rank = card.slice(0, -1);

  const suitColors: Record<string, string> = {
    h: "text-red-600",
    d: "text-red-600",
    c: "text-black",
    s: "text-black",
  };

  const suitSymbols: Record<string, string> = {
    h: "♥",
    d: "♦",
    c: "♣",
    s: "♠",
  };

  const sizeClasses = {
    sm: "w-10 h-14 text-xs",
    md: "w-12 h-18 text-sm",
    lg: "w-16 h-24 text-base",
  };

  return (
    <div
      className={`
        ${sizeClasses[size]}
        bg-white border-2 rounded-lg cursor-pointer transition-all duration-200
        flex flex-col items-center justify-center text-center
        ${
          isSelected
            ? "border-yellow-400 bg-yellow-100 shadow-lg"
            : "border-gray-300"
        }
        ${
          isHovered
            ? "border-blue-400 shadow-md transform -translate-y-1 z-50"
            : ""
        }
        ${className}
      `}
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      <div className={`font-bold ${suitColors[suit]}`}>
        {rank.toUpperCase()}
      </div>
      <div className={`text-lg ${suitColors[suit]}`}>{suitSymbols[suit]}</div>
    </div>
  );
}
