import { Button } from "./ui/button";
import { Play } from "lucide-react";

interface PassCardsButtonProps {
  cardToNextSeat: string | null;
  cardToPrevSeat: string | null;
  onPass: () => void;
  isPending: boolean;
}

export function PassCardsButton({
  cardToNextSeat,
  cardToPrevSeat,
  onPass,
  isPending,
}: PassCardsButtonProps) {
  if (!cardToNextSeat || !cardToPrevSeat) return null;

  return (
    <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-50">
      <Button
        onClick={onPass}
        disabled={isPending}
        className="h-16 px-8 text-xl font-bold animate-pulse card-glow shadow-2xl"
        size="lg"
      >
        <Play className="h-6 w-6 mr-2" />
        {isPending ? "Passing Cards..." : "Pass Selected Cards"}
      </Button>
    </div>
  );
}

