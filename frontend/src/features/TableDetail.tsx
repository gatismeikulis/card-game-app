import { useNavigate, useParams } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { apiFetch } from "../api";
import { PlayerDetail } from "./PlayerDetail";

// Helper function to safely render any value
const safeRender = (value: any): string => {
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
};

// Helper function to get card color styling
const getCardStyle = (card: string) => {
  if (!card || card.length < 2) return "bg-gray-100 text-gray-600";

  const suit = card.slice(-1); // Last character is suit
  switch (suit) {
    case "s":
      return "bg-gray-100 text-black border-gray-300"; // spades - light gray background
    case "h":
      return "bg-red-100 text-red-800 border-red-300"; // hearts - light red background
    case "d":
      return "bg-blue-100 text-blue-800 border-blue-300"; // diamonds - light blue background
    case "c":
      return "bg-green-100 text-green-800 border-green-300"; // clubs - light green background
    default:
      return "bg-gray-100 text-gray-600";
  }
};

// Helper to render suit as a colored badge with full name
const renderSuitBadge = (value: any) => {
  if (!value)
    return (
      <span className="px-2 py-0.5 rounded border text-sm text-gray-500">
        N/A
      </span>
    );
  const sym = String(value).trim().toLowerCase();
  const map: Record<string, { name: string; cls: string }> = {
    s: { name: "SPADE", cls: "bg-gray-100 text-black border-gray-300" },
    h: { name: "HEART", cls: "bg-red-100 text-red-700 border-red-300" },
    d: { name: "DIAMOND", cls: "bg-blue-100 text-blue-700 border-blue-300" },
    c: { name: "CLUB", cls: "bg-green-100 text-green-700 border-green-300" },
  };
  const info = map[sym];
  if (!info)
    return (
      <span className="px-2 py-0.5 rounded border text-sm text-gray-500">
        N/A
      </span>
    );
  return (
    <span
      className={`px-2 py-0.5 rounded border text-sm font-medium ${info.cls}`}
    >
      {info.name}
    </span>
  );
};

export function TableDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [removeSeat, setRemoveSeat] = useState<string>("");
  const [botStrategy] = useState("Random");
  const [botSeat] = useState<string>("");
  const [bidAmount, setBidAmount] = useState<string>("");
  const [selectedCards, setSelectedCards] = useState<{
    cardToNextSeat: string | null;
    cardToPrevSeat: string | null;
  }>({
    cardToNextSeat: null,
    cardToPrevSeat: null,
  });
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["table", id],
    queryFn: () => apiFetch(`/api/v1/tables/${id}/`),
    enabled: !!id,
  });

  const refresh = () => {
    refetch();
    setErrorMessage(null);
  };

  const join = useMutation({
    mutationFn: () =>
      apiFetch(`/api/v1/tables/${id}/join/`, {
        method: "POST",
        body: JSON.stringify({}),
      }),
    onSuccess: () => {
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  const leave = useMutation({
    mutationFn: () =>
      apiFetch(`/api/v1/tables/${id}/leave/`, {
        method: "POST",
        body: JSON.stringify({}),
      }),
    onSuccess: () => {
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  const addBot = useMutation({
    mutationFn: () =>
      apiFetch(`/api/v1/tables/${id}/add-bot/`, {
        method: "POST",
        body: JSON.stringify({
          bot_strategy_kind: botStrategy,
          preferred_seat: botSeat ? Number(botSeat) : undefined,
        }),
      }),
    onSuccess: () => {
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  const removeBot = useMutation({
    mutationFn: () =>
      apiFetch(`/api/v1/tables/${id}/remove-bot/`, {
        method: "POST",
        body: JSON.stringify({ seat_number: Number(removeSeat) }),
      }),
    onSuccess: () => {
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  const startGame = useMutation({
    mutationFn: () =>
      apiFetch(`/api/v1/tables/${id}/start-game/`, {
        method: "POST",
        body: JSON.stringify({}),
      }),
    onSuccess: () => {
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  const takeTurn = useMutation({
    mutationFn: (command: { type: string; params: any }) =>
      apiFetch(`/api/v1/tables/${id}/take-turn/`, {
        method: "POST",
        body: JSON.stringify(command),
      }),
    onSuccess: () => {
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  const takeAutomaticTurn = useMutation({
    mutationFn: async () => {
      const result = await apiFetch(
        `/api/v1/tables/${id}/take-automatic-turn/`,
        {
          method: "POST",
        }
      );
      return result;
    },
    onSuccess: () => {
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      console.error("Take automatic turn error:", error);
      setErrorMessage(String(error));
    },
  });

  const passCards = useMutation({
    mutationFn: (cards: {
      card_to_next_seat: string;
      card_to_prev_seat: string;
    }) =>
      apiFetch(`/api/v1/tables/${id}/take-turn/`, {
        method: "POST",
        body: JSON.stringify({
          type: "pass_cards",
          params: cards,
        }),
      }),
    onSuccess: () => {
      setSelectedCards({ cardToNextSeat: null, cardToPrevSeat: null });
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div className="text-red-600">{String(error)}</div>;

  return (
    <div className="space-y-4">
      <button
        className="px-3 py-1 border rounded"
        onClick={() => navigate("/")}
      >
        Go to login page
      </button>
      <button
        className="px-3 py-1 border rounded"
        onClick={() => navigate("/tables")}
      >
        Go to tables page
      </button>
      {errorMessage && <p className="text-red-600 text-sm">{errorMessage}</p>}
      <div className="flex flex-wrap items-center gap-2">
        <button className="px-3 py-1 border rounded" onClick={() => refresh()}>
          Refresh
        </button>
        <button
          className="px-3 py-1 border rounded"
          onClick={() => join.mutate()}
        >
          Join
        </button>
        <button
          className="px-3 py-1 border rounded"
          onClick={() => leave.mutate()}
        >
          Leave
        </button>
        <button
          className="px-3 py-1 border rounded"
          onClick={() => startGame.mutate()}
        >
          Start Game
        </button>
      </div>
      <div className="bg-white border rounded p-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-gray-600">Status:</span>
          <span className="font-medium">{data.status}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-600">Summary:</span>
          <span className="font-medium">
            {data.game_state?.summary
              ? Object.entries(data.game_state.summary)
                  .map(([seat, points]) => {
                    const player = data.players?.find(
                      (p: any) => p.seat_number === parseInt(seat)
                    );
                    const playerName = player?.screen_name || `Seat ${seat}`;
                    return `${playerName}: ${points}`;
                  })
                  .join(", ")
              : "N/A"}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-600">Round:</span>
          <span className="font-medium">
            {safeRender(data.game_state?.round?.round_number)}
          </span>
        </div>
      </div>
      <div className="bg-white border rounded p-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-gray-600">Phase:</span>
          <span className="font-medium">
            {safeRender(data.game_state?.round?.phase)}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-600">Required Suit:</span>
          {renderSuitBadge(data.game_state?.round?.required_suit)}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-600">Trump Suit:</span>
          {renderSuitBadge(data.game_state?.round?.trump_suit)}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-600">Highest Bid:</span>
          <span className="font-medium">
            {data.game_state?.round?.highest_bid
              ? (() => {
                  const bid = data.game_state.round.highest_bid;
                  if (typeof bid === "object" && bid !== null) {
                    // Object has keys "0" (seat) and "1" (bid value)
                    if (bid["0"] !== undefined && bid["1"] !== undefined) {
                      const seatNumber = parseInt(bid["0"]);
                      const bidAmount = bid["1"];
                      const player = data.players?.find(
                        (p: any) => p.seat_number === seatNumber
                      );
                      const playerName =
                        player?.screen_name || `Seat ${seatNumber}`;
                      return `${playerName}: ${bidAmount}`;
                    }
                  }
                  return safeRender(bid);
                })()
              : "N/A"}
          </span>
        </div>
        {data.game_state?.is_my_turn &&
          data.game_state?.round?.phase === "Bidding" && (
            <div className="flex items-center gap-2 pt-2 border-t">
              <span className="text-gray-600">Your Bid:</span>
              <input
                type="number"
                placeholder="Enter bid amount"
                className="border rounded px-2 py-1 w-32"
                min="0"
                value={bidAmount}
                onChange={(e) => setBidAmount(e.target.value)}
              />
              <button
                className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                onClick={() => {
                  if (bidAmount) {
                    takeTurn.mutate({
                      type: "make_bid",
                      params: { bid: Number(bidAmount) },
                    });
                    setBidAmount("");
                  }
                }}
                disabled={!bidAmount || takeTurn.isPending}
              >
                {takeTurn.isPending ? "Bidding..." : "BID"}
              </button>
            </div>
          )}
        {data.game_state?.round?.phase === "Forming Hands" &&
          data.game_state.is_my_turn && (
            <div className="flex items-center gap-2 pt-2 border-t">
              <span className="text-gray-600">Pass Cards:</span>
              <div className="flex items-center gap-2">
                <span className="text-sm">
                  Next Seat: {selectedCards.cardToNextSeat || "Select card"}
                </span>
                <span className="text-sm">
                  Prev Seat: {selectedCards.cardToPrevSeat || "Select card"}
                </span>
              </div>
              <button
                className="bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700"
                onClick={() => {
                  if (
                    selectedCards.cardToNextSeat &&
                    selectedCards.cardToPrevSeat
                  ) {
                    passCards.mutate({
                      card_to_next_seat: selectedCards.cardToNextSeat,
                      card_to_prev_seat: selectedCards.cardToPrevSeat,
                    });
                  }
                }}
                disabled={
                  !selectedCards.cardToNextSeat ||
                  !selectedCards.cardToPrevSeat ||
                  passCards.isPending
                }
              >
                {passCards.isPending ? "Passing..." : "Pass Cards"}
              </button>
            </div>
          )}
        {data.game_state && !data.game_state.is_my_turn && (
          <div className="flex items-center gap-2 pt-2 border-t">
            <span className="text-gray-600">Not your turn</span>
            <button
              className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
              onClick={() => takeAutomaticTurn.mutate()}
              disabled={takeAutomaticTurn.isPending}
            >
              {takeAutomaticTurn.isPending
                ? "Taking turn..."
                : "Take Automatic Turn"}
            </button>
          </div>
        )}
        {(data.game_state?.round?.cards_on_board &&
          Object.values(data.game_state.round.cards_on_board).some(
            (card) => card !== null
          )) ||
        !!data.game_state?.round?.prev_trick ? (
          <div className="flex gap-8 flex-wrap">
            {data.game_state?.round?.cards_on_board &&
              Object.values(data.game_state.round.cards_on_board).some(
                (card) => card !== null
              ) && (
                <div className="space-y-3">
                  <span className="text-gray-600 font-medium">
                    Cards on Board:
                  </span>
                  <div className="flex flex-wrap gap-3">
                    {Object.entries(data.game_state.round.cards_on_board)
                      .filter(([_, card]) => card !== null)
                      .map(([seat, card]) => {
                        const player = data.players?.find(
                          (p: any) => p.seat_number === parseInt(seat)
                        );
                        const playerName =
                          player?.screen_name || `Seat ${seat}`;
                        return (
                          <div
                            key={`${seat}-${card}`}
                            className="flex flex-col items-center gap-1"
                          >
                            <span className="text-xs text-gray-500 font-medium">
                              {playerName}
                            </span>
                            <div
                              className={`w-8 h-12 border-2 rounded flex items-center justify-center text-sm font-bold shadow-sm ${getCardStyle(
                                card as string
                              )}`}
                            >
                              {card as string}
                            </div>
                          </div>
                        );
                      })}
                  </div>
                </div>
              )}

            {(() => {
              const prevTrick: any = data.game_state?.round?.prev_trick;
              if (!prevTrick) return null;

              // Case 1: prev_trick has explicit structure { taken_by, cards }
              if (
                typeof prevTrick === "object" &&
                Array.isArray(prevTrick.cards)
              ) {
                const takenBySeatRaw: number | undefined =
                  typeof prevTrick.taken_by === "number"
                    ? prevTrick.taken_by
                    : undefined;
                // Prefer +1 mapping if zero-based index appears to be used and a player exists at +1
                const candidates = [
                  takenBySeatRaw,
                  takenBySeatRaw !== undefined ? takenBySeatRaw + 1 : undefined,
                ].filter((v): v is number => typeof v === "number");
                const takenByResolved = candidates.find((seatNum) =>
                  Boolean(
                    data.players?.some((p: any) => p.seat_number === seatNum)
                  )
                );
                const takenByName = takenByResolved
                  ? data.players?.find(
                      (p: any) => p.seat_number === takenByResolved
                    )?.screen_name || `Seat ${takenByResolved}`
                  : undefined;
                return (
                  <div className="ml-auto w-48 space-y-2">
                    <span className="text-gray-600 text-sm font-medium">
                      Previous Trick
                      {takenByName ? ` (Taken by: ${takenByName})` : ""}:
                    </span>
                    <div className="flex flex-wrap gap-2">
                      {prevTrick.cards.map((card: string, idx: number) => (
                        <div
                          key={`prev-${idx}-${card}`}
                          className={`w-6 h-9 border-2 rounded flex items-center justify-center text-xs font-bold shadow-sm ${getCardStyle(
                            card
                          )}`}
                        >
                          {card}
                        </div>
                      ))}
                    </div>
                  </div>
                );
              }

              // Case 2: prev_trick is a seat->card mapping like cards_on_board
              if (typeof prevTrick === "object") {
                const allKeys = Object.keys(prevTrick);
                const isZeroBased = allKeys.includes("0");
                const entries = Object.entries(prevTrick).filter(
                  ([_, card]) => card !== null
                );
                if (entries.length === 0) return null;
                return (
                  <div className="ml-auto w-48 space-y-2">
                    <span className="text-gray-600 text-sm font-medium">
                      Previous Trick:
                    </span>
                    <div className="flex flex-wrap gap-2">
                      {entries.map(([seat, card]) => {
                        const seatRaw = parseInt(seat);
                        const seatNumber = isZeroBased ? seatRaw + 1 : seatRaw;
                        const player = data.players?.find(
                          (p: any) => p.seat_number === seatNumber
                        );
                        const playerName =
                          player?.screen_name || `Seat ${seatNumber}`;
                        return (
                          <div
                            key={`prev-${seat}-${card}`}
                            className="flex flex-col items-center gap-1"
                          >
                            <span className="text-[10px] text-gray-500 font-medium">
                              {playerName}
                            </span>
                            <div
                              className={`w-6 h-9 border-2 rounded flex items-center justify-center text-xs font-bold shadow-sm ${getCardStyle(
                                card as string
                              )}`}
                            >
                              {card as string}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              }

              // Fallback: render safely
              return (
                <div className="ml-auto w-48 space-y-2">
                  <span className="text-gray-600 text-sm font-medium">
                    Previous Trick:
                  </span>
                  <div className="text-xs text-gray-700">
                    {safeRender(prevTrick)}
                  </div>
                </div>
              );
            })()}
          </div>
        ) : null}
      </div>
      {!data.game_state && (
        <div className="bg-white border rounded p-4">
          <div className="text-gray-600 font-medium mb-4">Table Seats</div>
          <div className="grid grid-cols-3 gap-4">
            {[1, 2, 3].map((seatNum) => {
              const player = data.players?.find(
                (p: any) => p.seat_number === seatNum
              );
              const isSeatTaken = !!player;

              return (
                <div key={seatNum} className="border rounded p-3 text-center">
                  <div className="text-sm text-gray-600 mb-2">
                    Seat {seatNum}
                  </div>
                  {isSeatTaken ? (
                    <div className="space-y-2">
                      <div className="font-medium">{player.screen_name}</div>
                      <div className="text-xs text-gray-500">
                        {player.bot_strategy_kind
                          ? `Bot (${player.bot_strategy_kind})`
                          : "Human"}
                      </div>
                      {player.bot_strategy_kind && (
                        <button
                          className="bg-red-600 text-white px-2 py-1 rounded text-xs hover:bg-red-700"
                          onClick={() => {
                            setRemoveSeat(seatNum.toString());
                            removeBot.mutate();
                          }}
                          disabled={removeBot.isPending}
                        >
                          {removeBot.isPending ? "Removing..." : "Remove Bot"}
                        </button>
                      )}
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <div className="text-gray-400 text-sm">Empty Seat</div>
                      <div className="flex flex-col gap-1">
                        <button
                          className="bg-blue-600 text-white px-2 py-1 rounded text-xs hover:bg-blue-700"
                          onClick={() => join.mutate()}
                          disabled={join.isPending}
                        >
                          {join.isPending ? "Joining..." : "Join"}
                        </button>
                        <button
                          className="bg-green-600 text-white px-2 py-1 rounded text-xs hover:bg-green-700"
                          onClick={() => addBot.mutate()}
                          disabled={addBot.isPending}
                        >
                          {addBot.isPending ? "Adding..." : "Add Bot"}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
      {data.game_state?.round?.seat_infos ? (
        <div className="flex gap-4">
          {[1, 2, 3].map((seatNum) => {
            const seatInfo = data.game_state?.round?.seat_infos?.[seatNum];
            if (!seatInfo) return null;

            // Find the player with this seat number
            const player = data.players?.find(
              (p: any) => p.seat_number === seatNum
            );
            const screenName =
              player?.screen_name || seatInfo.screen_name || `Unknown`;

            // Check if this is the active player
            const isActive = data.game_state?.active_seat === seatNum;
            const isMyTurn = data.game_state?.is_my_turn && isActive;

            return (
              <div
                key={seatNum}
                className={`p-2 rounded ${
                  isActive
                    ? "border-2 border-blue-500 bg-blue-50"
                    : "border border-gray-200"
                }`}
              >
                <PlayerDetail
                  bid={seatInfo.bid ?? -1}
                  hand={seatInfo.hand ?? 0}
                  marriage_points={seatInfo.marriage_points ?? null}
                  points={seatInfo.points ?? 0}
                  trick_count={seatInfo.trick_count ?? 0}
                  screen_name={screenName}
                  onCardClick={(card) => {
                    const phase = data.game_state?.round?.phase;
                    console.log("Card clicked:", card, "Phase:", phase);
                    if (phase === "Forming Hands") {
                      // Handle card selection for passing
                      console.log("Forming hands - selecting card");
                      if (!selectedCards.cardToNextSeat) {
                        setSelectedCards((prev) => ({
                          ...prev,
                          cardToNextSeat: card,
                        }));
                      } else if (!selectedCards.cardToPrevSeat) {
                        setSelectedCards((prev) => ({
                          ...prev,
                          cardToPrevSeat: card,
                        }));
                      }
                    } else {
                      // Normal play card
                      console.log("Normal play card");
                      takeTurn.mutate({
                        type: "play_card",
                        params: { card: card },
                      });
                    }
                  }}
                  isMyTurn={isMyTurn}
                />
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-gray-500">No game state available</div>
      )}
      <details>
        <summary className="cursor-pointer text-sm">Raw</summary>
        <pre className="text-xs bg-white p-3 rounded border overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </details>
    </div>
  );
}
