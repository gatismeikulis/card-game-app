import { Card, CardContent } from "./ui/card";

interface CardSelectionInfoProps {
  cardToNextSeat: string | null;
  cardToPrevSeat: string | null;
}

export function CardSelectionInfo({
  cardToNextSeat,
  cardToPrevSeat,
}: CardSelectionInfoProps) {
  return (
    <Card className="border-primary/50">
      <CardContent className="pt-4">
        <div className="flex justify-center items-center gap-8 text-sm">
          <div className="text-center">
            <p className="text-muted-foreground mb-1">To Next Seat</p>
            <p className="font-medium text-lg">
              {cardToNextSeat || "❌ Select card"}
            </p>
          </div>
          <div className="text-center">
            <p className="text-muted-foreground mb-1">To Prev Seat</p>
            <p className="font-medium text-lg">
              {cardToPrevSeat || "❌ Select card"}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

