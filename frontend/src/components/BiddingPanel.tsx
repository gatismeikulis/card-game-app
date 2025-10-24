import { useState, useEffect } from "react";
import * as React from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Plus } from "lucide-react";

interface BiddingPanelProps {
  onBid: (amount: number) => void;
  isLoading?: boolean;
  minBid?: number;
  maxBid?: number;
  hasMarriage?: boolean; // Has KQ of same suit
  currentHighestBid?: number; // Current highest bid in the round
  currentHighestBidder?: string; // Name of current highest bidder
  biddingStatus?: Record<number, { bid?: number; passed?: boolean }>; // Bidding status for all players
  currentPlayerSeat?: number; // Current player's seat number
}

export function BiddingPanel({
  onBid,
  isLoading = false,
  minBid = 60,
  maxBid = 200,
  hasMarriage = false,
  currentHighestBid = 0,
  currentHighestBidder,
  biddingStatus = {},
  currentPlayerSeat,
}: BiddingPanelProps) {
  const effectiveMaxBid = maxBid;
  // Minimum bid must be at least 5 points higher than current highest
  const effectiveMinBid =
    currentHighestBid > 0 ? currentHighestBid + 5 : minBid;

  // Check if bidding is possible
  const canBid = effectiveMinBid <= effectiveMaxBid;

  const [bidAmount, setBidAmount] = useState(
    canBid ? effectiveMinBid : effectiveMaxBid,
  );
  const [displayBid, setDisplayBid] = useState(
    canBid ? effectiveMinBid : effectiveMaxBid,
  );

  // Update bid amount when minimum changes
  React.useEffect(() => {
    if (canBid && bidAmount < effectiveMinBid) {
      setBidAmount(effectiveMinBid);
    }
  }, [effectiveMinBid, bidAmount, canBid]);

  // Smooth animation for display value
  useEffect(() => {
    const step = (bidAmount - displayBid) / 10;
    if (Math.abs(step) > 0.1) {
      const timer = setTimeout(() => {
        setDisplayBid((prev) => {
          const newVal = prev + step;
          if (Math.abs(newVal - bidAmount) < 1) return bidAmount;
          return newVal;
        });
      }, 20);
      return () => clearTimeout(timer);
    } else {
      setDisplayBid(bidAmount);
    }
  }, [bidAmount, displayBid]);

  const handleIncrease = (amount: number) => {
    setBidAmount((prev) => Math.min(effectiveMaxBid, prev + amount));
  };

  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBidAmount(Number(e.target.value));
  };

  const handleBid = () => {
    onBid(bidAmount);
  };

  // Check if current player has already bid and all others have passed
  const currentPlayerStatus = currentPlayerSeat
    ? biddingStatus[currentPlayerSeat]
    : null;
  const hasCurrentPlayerBid =
    currentPlayerStatus?.bid !== undefined && currentPlayerStatus.bid > 0;
  const allOthersPassed = Object.entries(biddingStatus).every(
    ([seat, status]) => {
      const seatNum = parseInt(seat);
      return (
        seatNum === currentPlayerSeat ||
        status.passed === true ||
        (status.bid !== undefined && status.bid < 0)
      );
    },
  );
  const shouldShowConfirm = hasCurrentPlayerBid && allOthersPassed;

  // If can't bid, show only pass option
  if (!canBid) {
    return (
      <Card className="card-glow border-destructive/50">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg text-destructive">
            Cannot Bid Higher
          </CardTitle>
          <p className="text-xs text-muted-foreground">
            Current: {currentHighestBid}{" "}
            {currentHighestBidder && `(${currentHighestBidder})`}
          </p>
          <p className="text-xs text-muted-foreground">
            Your max is {effectiveMaxBid} {!hasMarriage && "(no marriage)"}
          </p>
        </CardHeader>
        <CardContent>
          <Button
            variant="outline"
            onClick={() => onBid(-1)}
            disabled={isLoading}
            className="w-full h-12"
          >
            Pass (Can't bid higher)
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="card-glow border-primary/50">
      <CardHeader className="pb-2 sm:pb-3">
        <CardTitle className="text-sm sm:text-lg text-primary">
          Place Your Bid
        </CardTitle>
        {currentHighestBid > 0 && (
          <div className="space-y-1">
            <p className="text-sm font-semibold text-primary">
              Current Highest: {currentHighestBid}
            </p>
            {currentHighestBidder && (
              <p className="text-xs text-muted-foreground">
                by {currentHighestBidder}
              </p>
            )}
          </div>
        )}
      </CardHeader>
      <CardContent className="space-y-1 sm:space-y-2">
        {/* Large animated bid display */}
        <div className="text-center">
          <div className="text-2xl sm:text-4xl font-bold text-primary animate-pulse">
            {Math.round(displayBid)}
          </div>
          {!shouldShowConfirm && (
            <div className="text-xs sm:text-sm text-muted-foreground mt-1">
              Range: {effectiveMinBid} - {effectiveMaxBid}
            </div>
          )}
        </div>

        {/* Slider - Hide in CONFIRM phase */}
        {!shouldShowConfirm && (
          <div className="space-y-2">
            <input
              type="range"
              min={effectiveMinBid}
              max={effectiveMaxBid}
              step="5"
              value={bidAmount}
              onChange={handleSliderChange}
              className="w-full h-3 bg-muted rounded-lg appearance-none cursor-pointer slider-primary"
              disabled={isLoading}
            />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>{effectiveMinBid}</span>
              <span>{effectiveMaxBid}</span>
            </div>
          </div>
        )}

        {/* Quick adjust buttons - Show in both phases */}
        <div className="grid grid-cols-2 gap-2">
          <div className="space-y-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleIncrease(5)}
              disabled={bidAmount >= effectiveMaxBid || isLoading}
              className="w-full"
            >
              <Plus className="h-4 w-4 ml-1" />5
            </Button>
          </div>
          <div className="space-y-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleIncrease(10)}
              disabled={bidAmount >= effectiveMaxBid || isLoading}
              className="w-full"
            >
              <Plus className="h-4 w-4 ml-1" />
              10
            </Button>
          </div>
        </div>

        {/* Submit bid button */}
        {shouldShowConfirm ? (
          <Button
            onClick={() => onBid(-1)}
            disabled={isLoading}
            className="w-full h-8 sm:h-12 text-sm sm:text-lg font-bold bg-green-600 hover:bg-green-700"
            size="sm"
          >
            {isLoading ? "Confirming..." : `CONFIRM ${currentHighestBid}`}
          </Button>
        ) : (
          <Button
            onClick={handleBid}
            disabled={isLoading}
            className="w-full h-8 sm:h-12 text-sm sm:text-lg font-bold"
            size="sm"
          >
            {isLoading ? "Placing Bid..." : `Bid ${bidAmount}`}
          </Button>
        )}

        {/* Pass button */}
        {shouldShowConfirm ? (
          <Button
            variant="outline"
            onClick={() => onBid(bidAmount)}
            disabled={isLoading}
            className="w-full h-8 sm:h-10 text-xs sm:text-sm"
            size="sm"
          >
            Bid {bidAmount}
          </Button>
        ) : (
          <Button
            variant="outline"
            onClick={() => onBid(-1)}
            disabled={isLoading}
            className="w-full h-8 sm:h-10"
            size="sm"
          >
            Pass
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
