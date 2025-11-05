/**
 * Utility functions for game-related operations
 */

/**
 * Safely render any value as a string
 */
export function safeRender(value: unknown): string {
  if (value === null || value === undefined) return "N/A";
  if (
    typeof value === "string" ||
    typeof value === "number" ||
    typeof value === "boolean"
  ) {
    return String(value);
  }
  if (typeof value === "object") {
    return `Object (${Object.keys(value).length} keys)`;
  }
  return String(value);
}

/**
 * Check if a hand contains a marriage (King and Queen of the same suit)
 */
export function checkForMarriage(hand: string[] | number): boolean {
  if (
    typeof hand === "number" ||
    !hand ||
    !Array.isArray(hand) ||
    hand.length === 0
  ) {
    return false;
  }

  const suits = ["h", "d", "s", "c"];

  for (const suit of suits) {
    const hasKing = hand.some((card) => card.toLowerCase() === `k${suit}`);
    const hasQueen = hand.some((card) => card.toLowerCase() === `q${suit}`);
    if (hasKing && hasQueen) return true;
  }

  return false;
}

/**
 * Get suit badge styling information
 */
export function getSuitBadgeInfo(suit: string | null | undefined) {
  if (!suit) {
    return {
      name: "N/A",
      className: "bg-gray-500 text-gray-500",
    };
  }

  const sym = String(suit).trim().toLowerCase();
  const map: Record<string, { name: string; className: string }> = {
    s: { name: "SPADE", className: "bg-gray-100 text-black border-gray-300" },
    h: { name: "HEART", className: "bg-red-100 text-red-700 border-red-300" },
    d: { name: "DIAMOND", className: "bg-blue-100 text-blue-700 border-blue-300" },
    c: { name: "CLUB", className: "bg-green-100 text-green-700 border-green-300" },
  };

  return map[sym] || { name: "N/A", className: "bg-gray-500 text-gray-500" };
}

/**
 * Extract bidding status from game state
 */
export function extractBiddingStatus(
  seatInfos: Record<string, any> | undefined
): Record<number, { bid?: number; passed?: boolean }> {
  const status: Record<number, { bid?: number; passed?: boolean }> = {};

  if (!seatInfos) return status;

  Object.entries(seatInfos).forEach(([seat, info]: [string, any]) => {
    const seatNum = parseInt(seat);
    if (info.bid !== undefined) {
      status[seatNum] = { bid: info.bid };
    } else if (info.passed === true) {
      status[seatNum] = { passed: true };
    }
  });

  return status;
}

/**
 * Extract highest bid information
 */
export function extractHighestBid(
  highestBid: any,
  players: any[]
): { bidder: string; amount: number } | undefined {
  if (!highestBid || typeof highestBid !== "object") return undefined;

  if (highestBid["0"] !== undefined && highestBid["1"] !== undefined) {
    const seatNumber = parseInt(highestBid["0"]);
    const bidAmount = highestBid["1"];
    const player = players?.find((p: any) => p.seat_number === seatNumber);
    const playerName = player?.screen_name || `Seat ${seatNumber}`;
    return { bidder: playerName, amount: bidAmount };
  }

  return undefined;
}

/**
 * Process players data with game state information
 */
export function processPlayers(players: any[], gameState: any) {
  return (players || []).map((player: any) => {
    const seatInfo = gameState?.round?.seat_infos?.[player.seat_number];
    const hand = seatInfo?.hand;

    let hand_size = 0;
    if (typeof hand === "number") {
      hand_size = hand;
    } else if (Array.isArray(hand)) {
      hand_size = hand.length;
    }

    return {
      ...player,
      name: player.screen_name || player.name || `Player ${player.seat_number}`,
      hand_size: hand_size,
      tricks_taken: seatInfo?.trick_count || 0,
      bid: seatInfo?.bid || undefined,
      running_points: seatInfo?.points || undefined,
      marriage_points: seatInfo?.marriage_points || undefined,
      hand: hand,
    };
  });
}

