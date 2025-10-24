import { PlayingCard } from "./PlayingCard";

interface PlayerHandProps {
  cards: string[];
  selectedCards: string[];
  hoveredCard: string | null;
  onCardClick: (card: string) => void;
  onCardHover: (card: string | null) => void;
  className?: string;
}

export function PlayerHand({
  cards,
  selectedCards,
  hoveredCard,
  onCardClick,
  onCardHover,
  className = "",
}: PlayerHandProps) {
  return (
    <div className={`flex justify-center gap-0 sm:gap-1 ${className}`}>
      {cards.map((card) => (
        <PlayingCard
          key={card}
          card={card}
          isSelected={selectedCards.includes(card)}
          isHovered={hoveredCard === card}
          onClick={() => onCardClick(card)}
          onMouseEnter={() => onCardHover(card)}
          onMouseLeave={() => onCardHover(null)}
          size="lg"
          className="hover:scale-110 hover:-translate-y-2 transition-all duration-200 -ml-3 first:ml-0 shadow-lg hover:shadow-xl"
        />
      ))}
    </div>
  );
}
