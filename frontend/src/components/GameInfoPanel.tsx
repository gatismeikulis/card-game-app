import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { getSuitBadgeInfo, extractHighestBid, safeRender } from "../utils/gameUtils";

interface GameInfoPanelProps {
  phase: string;
  requiredSuit: string | null | undefined;
  trumpSuit: string | null | undefined;
  highestBid: any;
  players: any[];
  prevTrick: any[] | undefined;
}

export function GameInfoPanel({
  phase,
  requiredSuit,
  trumpSuit,
  highestBid,
  players,
  prevTrick,
}: GameInfoPanelProps) {
  const requiredSuitInfo = getSuitBadgeInfo(requiredSuit);
  const trumpSuitInfo = getSuitBadgeInfo(trumpSuit);
  const highestBidInfo = extractHighestBid(highestBid, players);

  const getCardColor = (suit: string) => {
    if (suit === "h" || suit === "d") {
      return "bg-red-100 text-red-800 border-red-300";
    } else if (suit === "s" || suit === "c") {
      return "bg-gray-100 text-gray-800 border-gray-300";
    }
    return "bg-background text-foreground border";
  };

  return (
    <Card className="card-glow">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">Game Info</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 text-sm">
        <div>
          <span className="text-muted-foreground">Phase:</span>
          <p className="font-semibold">{phase || "N/A"}</p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <span className="text-muted-foreground text-xs">Required:</span>
            <div className="mt-1">
              <span
                className={`px-2 py-0.5 rounded border text-sm font-medium ${requiredSuitInfo.className}`}
              >
                {requiredSuitInfo.name}
              </span>
            </div>
          </div>
          <div>
            <span className="text-muted-foreground text-xs">Trump:</span>
            <div className="mt-1">
              <span
                className={`px-2 py-0.5 rounded border text-sm font-medium ${trumpSuitInfo.className}`}
              >
                {trumpSuitInfo.name}
              </span>
            </div>
          </div>
        </div>

        {highestBidInfo && (
          <div>
            <span className="text-muted-foreground">Highest Bid:</span>
            <p className="font-semibold">
              {highestBidInfo.bidder}: {highestBidInfo.amount}
            </p>
          </div>
        )}

        {prevTrick && Array.isArray(prevTrick) && prevTrick.length > 0 && (
          <div className="pt-3 border-t">
            <div className="space-y-2">
              <h4 className="text-sm font-semibold text-primary">Last Trick</h4>
              <div className="text-xs border rounded p-2 bg-muted/50">
                <div className="mt-1 flex flex-wrap gap-1">
                  {prevTrick.map((card: any, idx: number) => {
                    const cardStr = String(card);
                    const suit = cardStr.slice(-1);
                    const cardColor = getCardColor(suit);

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
          </div>
        )}
      </CardContent>
    </Card>
  );
}

