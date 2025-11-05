import { useState, useCallback } from "react";

interface SelectedCards {
  cardToNextSeat: string | null;
  cardToPrevSeat: string | null;
}

export function useCardSelection() {
  const [selectedCards, setSelectedCards] = useState<SelectedCards>({
    cardToNextSeat: null,
    cardToPrevSeat: null,
  });

  const handleCardClick = useCallback(
    (
      card: string,
      phase: string,
      isMyTurn: boolean,
      onPlayCard: (card: string) => void
    ) => {
      if (!isMyTurn || phase === "Bidding") {
        return;
      }

      if (phase === "Forming Hands") {
        setSelectedCards((prev) => {
          // Toggle selection if already selected
          if (prev.cardToNextSeat === card) {
            return { ...prev, cardToNextSeat: null };
          }
          if (prev.cardToPrevSeat === card) {
            return { ...prev, cardToPrevSeat: null };
          }
          // Select first available slot
          if (!prev.cardToNextSeat) {
            return { ...prev, cardToNextSeat: card };
          }
          if (!prev.cardToPrevSeat) {
            return { ...prev, cardToPrevSeat: card };
          }
          return prev;
        });
      } else {
        // Normal play - immediate action
        onPlayCard(card);
      }
    },
    []
  );

  const clearSelection = useCallback(() => {
    setSelectedCards({ cardToNextSeat: null, cardToPrevSeat: null });
  }, []);

  return {
    selectedCards,
    handleCardClick,
    clearSelection,
  };
}

