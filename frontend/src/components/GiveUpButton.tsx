import { Button } from "./ui/button";
import { AlertTriangle } from "lucide-react";

interface GiveUpButtonProps {
  onGiveUp: () => void;
  isPending: boolean;
}

export function GiveUpButton({ onGiveUp, isPending }: GiveUpButtonProps) {
  return (
    <div className="absolute top-4 right-4 z-50">
      <Button
        onClick={onGiveUp}
        disabled={isPending}
        variant="destructive"
        size="lg"
        className="shadow-lg"
      >
        <AlertTriangle className="h-5 w-5 mr-2" />
        {isPending ? "Giving Up..." : "Give Up"}
      </Button>
    </div>
  );
}

