import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";

interface BotTurnButtonProps {
  onTakeTurn: () => void;
  isPending: boolean;
  className?: string;
}

export function BotTurnButton({
  onTakeTurn,
  isPending,
  className = "",
}: BotTurnButtonProps) {
  return (
    <Card className={className}>
      <CardContent className="pt-4">
        <div className="space-y-2">
          <div className="text-xs text-blue-600 font-medium">
            ⚡ Bot's turn - Click to advance
          </div>
          <Button
            onClick={onTakeTurn}
            disabled={isPending}
            size="sm"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white"
          >
            {isPending ? "Processing..." : "🤖 Take Bot Turn"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

