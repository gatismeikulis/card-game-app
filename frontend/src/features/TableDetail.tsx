import { useNavigate, useParams } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, useEffect } from "react";
import { apiFetch } from "../api";
import { GameBoard } from "../components/GameBoard";
import { BiddingPanel } from "../components/BiddingPanel";
import { Button } from "../components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { useUserData } from "../contexts/UserContext";
import { RefreshCw, LogOut, Play } from "lucide-react";

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

// Check if hand has a marriage (KQ of same suit)
const checkForMarriage = (hand: string[] | number): boolean => {
  // If hand is a number (for other players), we can't check for marriage
  if (
    typeof hand === "number" ||
    !hand ||
    !Array.isArray(hand) ||
    hand.length === 0
  )
    return false;

  const suits = ["h", "d", "s", "c"];

  for (const suit of suits) {
    const hasKing = hand.some((card) => card.toLowerCase() === `k${suit}`);
    const hasQueen = hand.some((card) => card.toLowerCase() === `q${suit}`);
    if (hasKing && hasQueen) return true;
  }

  return false;
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
  const queryClient = useQueryClient();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [selectedCards, setSelectedCards] = useState<{
    cardToNextSeat: string | null;
    cardToPrevSeat: string | null;
  }>({
    cardToNextSeat: null,
    cardToPrevSeat: null,
  });
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);

  // Get current user data from context - MUST be called before any early returns
  const { userId } = useUserData();

  const { data, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ["table", id],
    queryFn: () => apiFetch(`/api/v1/tables/${id}/`),
    enabled: !!id,
    staleTime: 0, // Always consider data stale
    gcTime: 0, // Don't cache data at all
    refetchOnWindowFocus: true, // Refetch when window gains focus
    refetchOnMount: true, // Always refetch on mount
    refetchInterval: (query) => {
      // Poll every 1 second during active games for real-time updates
      // Stop polling if game is finished or not started
      const gameData = query.state.data as any;
      if (!gameData) return 1000; // Poll every second while loading

      const isActive = gameData.status === "in_progress" && gameData.game_state;
      const isFinished =
        gameData.status === "FINISHED" || gameData.game_state?.is_finished;

      // Poll every 2 second during active gameplay for real-time updates
      if (isActive && !isFinished) return 2000;

      // Poll every 5 seconds while waiting for game to start
      if (gameData.status === "not_started") return 5000;

      // Stop polling for finished games
      return false;
    },
  });

  const refresh = () => {
    refetch();
    setErrorMessage(null);
  };

  const join = useMutation({
    mutationFn: (seatNumber: number | null) =>
      apiFetch(`/api/v1/tables/${id}/join/`, {
        method: "POST",
        body: JSON.stringify({
          preferred_seat: seatNumber ?? undefined,
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
    mutationFn: (seatNumber: number) =>
      apiFetch(`/api/v1/tables/${id}/add-bot/`, {
        method: "POST",
        body: JSON.stringify({
          bot_strategy_kind: "random",
          preferred_seat: seatNumber,
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
    mutationFn: (seatNumber: number) =>
      apiFetch(`/api/v1/tables/${id}/remove-bot/`, {
        method: "POST",
        body: JSON.stringify({ seat_number: seatNumber }),
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
      queryClient.invalidateQueries({ queryKey: ["table", id] });
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
        },
      );
      return result;
    },
    onSuccess: () => {
      refetch();
      queryClient.invalidateQueries({ queryKey: ["table", id] });
      setErrorMessage(null);
    },
    onError: (error) => {
      console.error("Take automatic turn error:", error);
      setErrorMessage(String(error));
    },
  });

  // Track when 3 cards were placed to ensure they stay visible for 1 second
  const [threeCardsPlacedAt, setThreeCardsPlacedAt] = useState<number | null>(
    null,
  );

  // Detect when 3 cards are on board
  useEffect(() => {
    if (!data?.game_state?.round?.cards_on_board) return;

    const cardsOnBoard = data.game_state.round.cards_on_board || {};
    const cardsPlayed = Object.values(cardsOnBoard).filter(
      (card) => card !== null,
    ).length;

    if (cardsPlayed === 3 && threeCardsPlacedAt === null) {
      // 3 cards just placed, record the time
      setThreeCardsPlacedAt(Date.now());
    } else if (cardsPlayed !== 3) {
      // Reset when cards are cleared
      setThreeCardsPlacedAt(null);
    }
  }, [data?.game_state?.round?.cards_on_board, threeCardsPlacedAt]);

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

  if (isLoading)
    return (
      <div className="min-h-screen game-gradient flex items-center justify-center">
        <div className="text-lg">Loading game...</div>
      </div>
    );

  if (error)
    return (
      <div className="min-h-screen game-gradient flex items-center justify-center">
        <div className="text-destructive text-lg">{String(error)}</div>
      </div>
    );

  // Check if game is finished
  const isGameFinished =
    data?.status === "FINISHED" || data?.game_state?.is_finished;

  // Extract player hand for current user
  const currentUser = data.players?.find((p: any) => p.user_id === userId);
  const currentUserSeat = currentUser?.seat_number;
  const currentPlayerSeatInfo = currentUserSeat
    ? data.game_state?.round?.seat_infos?.[currentUserSeat]
    : null;
  const playerHand = currentPlayerSeatInfo?.hand || [];
  // Prepare cards on board
  const cardsOnBoard = data.game_state?.round?.cards_on_board || {};

  // Get current phase
  const currentPhase = data.game_state?.round?.phase || "";

  // Extract bidding status for all players
  const biddingStatus = (() => {
    const status: Record<number, { bid?: number; passed?: boolean }> = {};

    // Get bidding information from seat_infos
    if (data.game_state?.round?.seat_infos) {
      Object.entries(data.game_state.round.seat_infos).forEach(
        ([seat, info]: [string, any]) => {
          const seatNum = parseInt(seat);
          if (info.bid !== undefined) {
            status[seatNum] = { bid: info.bid };
          } else if (info.passed === true) {
            status[seatNum] = { passed: true };
          }
        },
      );
    }

    return status;
  })();

  // Prepare selected cards for visual feedback
  const selectedCardsList = [
    selectedCards.cardToNextSeat,
    selectedCards.cardToPrevSeat,
  ].filter(Boolean) as string[];

  // Process players data with additional information
  const processedPlayers = (data.players || []).map((player: any) => {
    const seatInfo = data.game_state?.round?.seat_infos?.[player.seat_number];
    const hand = seatInfo?.hand;

    // Handle hand_size - can be integer or array
    let hand_size = 0;
    if (typeof hand === "number") {
      hand_size = hand;
    } else if (Array.isArray(hand)) {
      hand_size = hand.length;
    }

    return {
      ...player,
      hand_size: hand_size,
      tricks_taken: seatInfo?.trick_count || 0,
      bid: seatInfo?.bid || undefined,
      running_points: seatInfo?.points || undefined,
      marriage_points: seatInfo?.marriage_points || undefined,
      hand: hand, // Pass the actual hand data
    };
  });

  return (
    <div className="min-h-screen game-gradient">
      <div className="max-w-7xl mx-auto p-4 space-y-4">
        {/* Header with navigation and actions */}
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => refresh()}
              disabled={isFetching}
            >
              <RefreshCw
                className={`mr-2 h-4 w-4 ${isFetching ? "animate-spin" : ""}`}
              />
              {isFetching ? "Fetching..." : "Refresh"}
            </Button>
          </div>
          <div className="flex gap-2">
            {!data.game_state && (
              <>
                <Button
                  size="sm"
                  onClick={() => join.mutate(null)}
                  disabled={
                    data.players?.length >= (data.max_players || 3) ||
                    data.players.some((p: any) => p.user_id === userId)
                  }
                >
                  Join Table
                </Button>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => startGame.mutate()}
                  disabled={data.players?.length < (data.min_players || 3)}
                >
                  <Play className="mr-2 h-4 w-4" />
                  Start Game
                </Button>
              </>
            )}
            <Button
              size="sm"
              variant="outline"
              onClick={() => navigate("/tables")}
            >
              <LogOut className="mr-2 h-4 w-4" />
              Return
            </Button>
          </div>
        </div>

        {errorMessage && (
          <Card className="border-destructive">
            <CardContent className="pt-6">
              <p className="text-destructive text-sm">{errorMessage}</p>
            </CardContent>
          </Card>
        )}

        {/* Game Finished Message */}
        {isGameFinished && (
          <Card className="border-amber-500/50 bg-amber-500/10 card-glow">
            <CardHeader>
              <CardTitle className="text-2xl text-amber-500 flex items-center gap-2">
                🏆 Game Finished!
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">Final Scores:</h3>
                <div className="space-y-2">
                  {data.game_state?.summary
                    ? Object.entries(data.game_state.summary)
                        .sort(
                          ([, a]: any, [, b]: any) =>
                            (b as number) - (a as number),
                        )
                        .map(([seat, points]: [string, any]) => {
                          const player = data.players?.find(
                            (p: any) => p.seat_number === parseInt(seat),
                          );
                          const playerName =
                            player?.screen_name || `Seat ${seat}`;
                          const allScores = Object.values(
                            data.game_state.summary,
                          ) as number[];
                          const isWinner = points === Math.max(...allScores);
                          return (
                            <div
                              key={seat}
                              className={`flex justify-between items-center p-2 rounded ${
                                isWinner
                                  ? "bg-amber-500/20 border border-amber-500/50"
                                  : "bg-muted/50"
                              }`}
                            >
                              <span
                                className={`font-medium ${
                                  isWinner ? "text-amber-500" : ""
                                }`}
                              >
                                {isWinner && "👑 "}
                                {playerName}
                              </span>
                              <span
                                className={`font-bold text-lg ${
                                  isWinner ? "text-amber-500" : ""
                                }`}
                              >
                                {String(points)}
                              </span>
                            </div>
                          );
                        })
                    : "No scores available"}
                </div>
              </div>
              <div className="flex gap-2">
                <Button
                  className="flex-1"
                  onClick={() => startGame.mutate()}
                  disabled={startGame.isPending}
                >
                  <Play className="mr-2 h-4 w-4" />
                  {startGame.isPending ? "Starting..." : "Start New Game"}
                </Button>
                <Button variant="outline" onClick={() => navigate("/tables")}>
                  Back to Tables
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Game Canvas and Info - Three column layout */}
        {data.game_state && (
          <div className="flex flex-col lg:flex-row gap-4 items-stretch w-full min-h-0">
            {/* Canvas - Main game area */}
            <div className="flex-1 flex justify-center relative min-w-0 w-full lg:w-auto">
              {/* Pass Cards Button - Prominent overlay during Forming Hands phase */}
              {data.game_state?.is_my_turn &&
                data.game_state?.round?.phase === "Forming Hands" &&
                selectedCards.cardToNextSeat &&
                selectedCards.cardToPrevSeat && (
                  <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-50">
                    <Button
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
                      disabled={passCards.isPending}
                      className="h-16 px-8 text-xl font-bold animate-pulse card-glow shadow-2xl"
                      size="lg"
                    >
                      <Play className="h-6 w-6 mr-2" />
                      {passCards.isPending
                        ? "Passing Cards..."
                        : "Pass Selected Cards"}
                    </Button>
                  </div>
                )}

              <GameBoard
                players={processedPlayers}
                currentUserSeat={currentUserSeat}
                currentUserHand={playerHand}
                selectedCards={selectedCardsList}
                hoveredCard={hoveredCard}
                onCardClick={(card) => {
                  // Don't allow card clicks when it's not the player's turn
                  if (!data.game_state?.is_my_turn) {
                    return;
                  }

                  const phase = data.game_state?.round?.phase;

                  // Don't allow card clicks during bidding phase
                  if (phase === "Bidding") {
                    return;
                  }

                  if (phase === "Forming Hands") {
                    // Toggle card selection - click again to deselect
                    if (selectedCards.cardToNextSeat === card) {
                      // Deselect cardToNextSeat
                      setSelectedCards((prev) => ({
                        ...prev,
                        cardToNextSeat: null,
                      }));
                    } else if (selectedCards.cardToPrevSeat === card) {
                      // Deselect cardToPrevSeat
                      setSelectedCards((prev) => ({
                        ...prev,
                        cardToPrevSeat: null,
                      }));
                    } else if (!selectedCards.cardToNextSeat) {
                      // Select as cardToNextSeat
                      setSelectedCards((prev) => ({
                        ...prev,
                        cardToNextSeat: card,
                      }));
                    } else if (!selectedCards.cardToPrevSeat) {
                      // Select as cardToPrevSeat
                      setSelectedCards((prev) => ({
                        ...prev,
                        cardToPrevSeat: card,
                      }));
                    }
                  } else {
                    // Normal play - immediate action
                    takeTurn.mutate({
                      type: "play_card",
                      params: { card: card },
                    });
                  }
                }}
                onCardHover={setHoveredCard}
                activeSeat={data.game_state.active_seat}
                phase={currentPhase}
                cardsOnBoard={cardsOnBoard}
                biddingPanel={
                  data.game_state?.is_my_turn &&
                  data.game_state?.round?.phase === "Bidding" ? (
                    <BiddingPanel
                      onBid={(amount) => {
                        takeTurn.mutate({
                          type: "make_bid",
                          params: { bid: amount },
                        });
                      }}
                      isLoading={takeTurn.isPending}
                      minBid={60}
                      maxBid={200}
                      hasMarriage={checkForMarriage(playerHand)}
                      currentHighestBid={(() => {
                        const bid = data.game_state?.round?.highest_bid;
                        if (
                          typeof bid === "object" &&
                          bid !== null &&
                          bid["1"] !== undefined
                        ) {
                          return Number(bid["1"]);
                        }
                        return 0;
                      })()}
                      currentHighestBidder={(() => {
                        const bid = data.game_state?.round?.highest_bid;
                        if (
                          typeof bid === "object" &&
                          bid !== null &&
                          bid["0"] !== undefined
                        ) {
                          const seatNumber = parseInt(bid["0"]);
                          const player = data.players?.find(
                            (p: any) => p.seat_number === seatNumber,
                          );
                          return player?.screen_name;
                        }
                        return undefined;
                      })()}
                      biddingStatus={biddingStatus}
                      currentPlayerSeat={currentUserSeat}
                    />
                  ) : null
                }
                playerStats={currentPlayerSeatInfo}
                requiredSuit={data.game_state?.round?.required_suit}
                trumpSuit={data.game_state?.round?.trump_suit}
                lastTrick={data.game_state?.round?.prev_trick}
                highestBid={(() => {
                  const bid = data.game_state?.round?.highest_bid;
                  if (
                    bid &&
                    typeof bid === "object" &&
                    bid["0"] !== undefined
                  ) {
                    const seatNumber = parseInt(bid["0"]);
                    const bidAmount = bid["1"];
                    const player = data.players?.find(
                      (p: any) => p.seat_number === seatNumber,
                    );
                    const playerName =
                      player?.screen_name || `Seat ${seatNumber}`;
                    return { bidder: playerName, amount: bidAmount };
                  }
                  return undefined;
                })()}
              />
            </div>

            {/* Mobile Bot Turn Button */}
            <div className="lg:hidden">
              {(() => {
                const activeSeat = data.game_state?.active_seat;
                const activePlayer = data.players?.find(
                  (p: any) => p.seat_number === activeSeat,
                );
                const isBotTurn = activePlayer?.bot_strategy_kind;

                if (!isBotTurn) return null;

                return (
                  <Card>
                    <CardContent className="pt-4">
                      <div className="space-y-2">
                        <div className="text-xs text-blue-600 font-medium">
                          ⚡ Bot's turn - Click to advance
                        </div>
                        <Button
                          onClick={() => takeAutomaticTurn.mutate()}
                          disabled={takeAutomaticTurn.isPending}
                          size="sm"
                          className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                        >
                          {takeAutomaticTurn.isPending
                            ? "Processing..."
                            : "🤖 Take Bot Turn"}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                );
              })()}
            </div>

            {/* Right Side Panel - Current Move, Game Info and Bot Controls */}
            <div className="hidden lg:block w-full lg:w-64 space-y-4 flex-shrink-0">
              {/* Game Phase Info */}
              <Card className="card-glow">
                <CardHeader className="pb-3">
                  <CardTitle className="text-lg">Game Info</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3 text-sm">
                  <div>
                    <span className="text-muted-foreground">Phase:</span>
                    <p className="font-semibold">{currentPhase || "N/A"}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <span className="text-muted-foreground text-xs">
                        Required:
                      </span>
                      <div className="mt-1">
                        {renderSuitBadge(data.game_state?.round?.required_suit)}
                      </div>
                    </div>
                    <div>
                      <span className="text-muted-foreground text-xs">
                        Trump:
                      </span>
                      <div className="mt-1">
                        {renderSuitBadge(data.game_state?.round?.trump_suit)}
                      </div>
                    </div>
                  </div>

                  {data.game_state?.round?.highest_bid && (
                    <div>
                      <span className="text-muted-foreground">
                        Highest Bid:
                      </span>
                      <p className="font-semibold">
                        {(() => {
                          const bid = data.game_state.round.highest_bid;
                          if (typeof bid === "object" && bid !== null) {
                            if (
                              bid["0"] !== undefined &&
                              bid["1"] !== undefined
                            ) {
                              const seatNumber = parseInt(bid["0"]);
                              const bidAmount = bid["1"];
                              const player = data.players?.find(
                                (p: any) => p.seat_number === seatNumber,
                              );
                              const playerName =
                                player?.screen_name || `Seat ${seatNumber}`;
                              return `${playerName}: ${bidAmount}`;
                            }
                          }
                          return safeRender(bid);
                        })()}
                      </p>
                    </div>
                  )}

                  {/* Last Trick */}
                  {data.game_state?.round?.prev_trick &&
                    Array.isArray(data.game_state.round.prev_trick) &&
                    data.game_state.round.prev_trick.length > 0 && (
                      <div className="pt-3 border-t">
                        <div className="space-y-2">
                          <h4 className="text-sm font-semibold text-primary">
                            Last Trick
                          </h4>
                          <div className="text-xs border rounded p-2 bg-muted/50">
                            <div className="mt-1 flex flex-wrap gap-1">
                              {data.game_state.round.prev_trick.map(
                                (card: any, idx: number) => {
                                  const cardStr = String(card);
                                  const suit = cardStr.slice(-1);
                                  let cardColor =
                                    "bg-background text-foreground border";

                                  if (suit === "h" || suit === "d") {
                                    cardColor =
                                      "bg-red-100 text-red-800 border-red-300";
                                  } else if (suit === "s" || suit === "c") {
                                    cardColor =
                                      "bg-gray-100 text-gray-800 border-gray-300";
                                  }

                                  return (
                                    <span
                                      key={idx}
                                      className={`text-sm px-2 py-1 rounded border font-bold ${cardColor}`}
                                    >
                                      {cardStr}
                                    </span>
                                  );
                                },
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                </CardContent>
              </Card>

              {/* Automatic Turn Button - Owner Only */}
              {data.game_state &&
                (data.owner_id === currentUser?.user_id ||
                  data.owner_id === currentUser?.id) && (
                  <Card>
                    <CardContent className="pt-4">
                      {(() => {
                        const activeSeat = data.game_state?.active_seat;
                        const activePlayer = data.players?.find(
                          (p: any) => p.seat_number === activeSeat,
                        );
                        const isBotTurn = activePlayer?.bot_strategy_kind;

                        if (!isBotTurn) return null;

                        return (
                          <div className="space-y-2">
                            <div className="text-xs text-blue-600 font-medium">
                              ⚡ Bot's turn - Click to advance
                            </div>
                            <Button
                              onClick={() => takeAutomaticTurn.mutate()}
                              disabled={takeAutomaticTurn.isPending}
                              size="sm"
                              className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                            >
                              {takeAutomaticTurn.isPending
                                ? "Processing..."
                                : "🤖 Take Bot Turn"}
                            </Button>
                          </div>
                        );
                      })()}
                    </CardContent>
                  </Card>
                )}
            </div>
          </div>
        )}

        {/* Game Status and Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Status</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg font-semibold">{data.status}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Round</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg font-semibold">
                {safeRender(data.game_state?.round?.round_number)}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Scores</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm space-y-1">
                {data.game_state?.summary
                  ? Object.entries(data.game_state.summary).map(
                      ([seat, points]) => {
                        const player = data.players?.find(
                          (p: any) => p.seat_number === parseInt(seat),
                        );
                        const playerName =
                          player?.screen_name || `Seat ${seat}`;
                        return (
                          <div key={seat} className="flex justify-between">
                            <span>{playerName}:</span>
                            <span className="font-semibold">
                              {String(points)}
                            </span>
                          </div>
                        );
                      },
                    )
                  : "No scores yet"}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Card Selection Info - During Forming Hands phase */}
        {data.game_state?.round?.phase === "Forming Hands" &&
          data.game_state?.is_my_turn && (
            <Card className="border-primary/50">
              <CardContent className="pt-4">
                <div className="flex justify-center items-center gap-8 text-sm">
                  <div className="text-center">
                    <p className="text-muted-foreground mb-1">To Next Seat</p>
                    <p className="font-medium text-lg">
                      {selectedCards.cardToNextSeat || "❌ Select card"}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-muted-foreground mb-1">To Prev Seat</p>
                    <p className="font-medium text-lg">
                      {selectedCards.cardToPrevSeat || "❌ Select card"}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

        {/* Table Seats - shown when game hasn't started */}
        {!data.game_state && (
          <Card>
            <CardHeader>
              <CardTitle>Table Seats</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[1, 2, 3].map((seatNum) => {
                  const player = data.players?.find(
                    (p: any) => p.seat_number === seatNum,
                  );
                  const isSeatTaken = !!player;
                  const isCurrentUser = player && !player.bot_strategy_kind;
                  const isBot = player && player.bot_strategy_kind;
                  const canJoin =
                    !isSeatTaken &&
                    data.players?.length < (data.max_players || 3) &&
                    !data.players.some((p: any) => p.user_id === userId);

                  return (
                    <Card key={seatNum} className="card-hover">
                      <CardContent className="pt-6 text-center">
                        <div className="text-sm text-muted-foreground mb-3">
                          Seat {seatNum}
                        </div>
                        {isSeatTaken ? (
                          <div className="space-y-3">
                            <div className="font-medium text-lg">
                              {player.screen_name}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {isBot
                                ? `Bot (${player.bot_strategy_kind})`
                                : "Human Player"}
                            </div>
                            {isBot && (
                              <Button
                                variant="destructive"
                                size="sm"
                                onClick={() => removeBot.mutate(seatNum)}
                                disabled={removeBot.isPending}
                                className="w-full"
                              >
                                {removeBot.isPending
                                  ? "Removing..."
                                  : "Remove Bot"}
                              </Button>
                            )}
                            {isCurrentUser && (
                              <Button
                                variant="destructive"
                                size="sm"
                                onClick={() => leave.mutate()}
                                disabled={leave.isPending}
                                className="w-full"
                              >
                                {leave.isPending ? "Leaving..." : "Leave Table"}
                              </Button>
                            )}
                          </div>
                        ) : (
                          <div className="space-y-2">
                            <div className="text-muted-foreground text-sm mb-3">
                              Empty Seat
                            </div>
                            <div className="flex flex-col gap-2">
                              <Button
                                size="sm"
                                onClick={() => join.mutate(seatNum)}
                                disabled={join.isPending || !canJoin}
                                className="w-full"
                              >
                                {join.isPending ? "Joining..." : "Join Table"}
                              </Button>
                              <Button
                                size="sm"
                                variant="secondary"
                                onClick={() => addBot.mutate(seatNum)}
                                disabled={addBot.isPending}
                                className="w-full"
                              >
                                {addBot.isPending ? "Adding..." : "Add Bot"}
                              </Button>
                            </div>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        )}
        {/* Debug: Raw data */}
        <details className="mt-4">
          <summary className="cursor-pointer text-sm text-muted-foreground hover:text-foreground">
            View Raw Data (Debug)
          </summary>
          <Card className="mt-2">
            <CardContent className="pt-6">
              <pre className="text-xs overflow-auto max-h-96">
                {JSON.stringify(data, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </details>
      </div>
    </div>
  );
}
