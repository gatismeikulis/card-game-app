import { useNavigate, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { useState, useEffect, useCallback } from "react";
import { apiFetch } from "../api";
import { GameBoard } from "../components/GameBoard";
import { BiddingPanel } from "../components/BiddingPanel";
import { GameFinishedCard } from "../components/GameFinishedCard";
import { GameStatusCards } from "../components/GameStatusCards";
import { TableSeats } from "../components/TableSeats";
import { CardSelectionInfo } from "../components/CardSelectionInfo";
import { GameInfoPanel } from "../components/GameInfoPanel";
import { BotTurnButton } from "../components/BotTurnButton";
import { TableHeader } from "../components/TableHeader";
import { ErrorMessage } from "../components/ErrorMessage";
import { PassCardsButton } from "../components/PassCardsButton";
import { GiveUpButton } from "../components/GiveUpButton";
import { Card, CardContent } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { useUserData } from "../contexts/UserContext";
import { useTableWebSocket } from "../hooks/useTableWebSocket";
import { useGameActions } from "../hooks/useGameActions";
import { useCardSelection } from "../hooks/useCardSelection";
import {
  checkForMarriage,
  extractBiddingStatus,
  extractHighestBid,
  processPlayers,
} from "../utils/gameUtils";

export function TableDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { userId, isLoggedIn } = useUserData();
  const [tableData, setTableData] = useState<any>(null);

  // Initial HTTP fetch to get table state
  const {
    data: initialData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["table", id],
    queryFn: () => apiFetch(`/api/v1/tables/${id}/`),
    enabled: !!id,
    staleTime: 0,
    gcTime: 0,
  });

  // Initialize table data from initial fetch
  useEffect(() => {
    if (initialData) {
      setTableData(initialData);
    }
  }, [initialData]);

  // WebSocket connection
  const handleWebSocketMessage = useCallback((message: any) => {
    if (message.type === "table_action") {
      // Full table data update
      if (message.data?.table_data) {
        setTableData(message.data.table_data);
      }
    } else if (message.type === "game_action") {
      // Partial update: only game_state and status
      if (message.data) {
        setTableData((prevData: any) => {
          if (!prevData) return prevData;
          return {
            ...prevData,
            game_state: message.data.game_state,
            status: message.data.table_status,
          };
        });
      }
    }
  }, []);

  const {
    connected: wsConnected,
    pending: wsPending,
    error: wsError,
    sendMessage,
  } = useTableWebSocket(id, !!initialData, handleWebSocketMessage);

  // Game actions
  const {
    join,
    leave,
    addBot,
    removeBot,
    startGame,
    takeTurn,
    takeAutomaticTurn,
    passCards,
    giveUp,
    cancelGame,
    abortGame,
  } = useGameActions({ sendMessage });

  // Card selection
  const { selectedCards, handleCardClick, clearSelection } = useCardSelection();
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);

  const handleCancelGame = useCallback(() => {
    if (
      typeof window !== "undefined" &&
      window.confirm(
        "Cancel the current game? This will end the game immediately for everyone."
      )
    ) {
      cancelGame();
    }
  }, [cancelGame]);

  const handleAbortPlayer = useCallback(
    (player: any) => {
      if (!player?.seat_number) return;
      const playerName =
        player.screen_name || player.name || `Seat ${player.seat_number}`;
      if (
        typeof window !== "undefined" &&
        window.confirm(
          `Abort the game and kick ${playerName}? This will end the current game immediately.`
        )
      ) {
        abortGame(player.seat_number);
      }
    },
    [abortGame]
  );

  // Handle passing cards
  const handlePassCards = () => {
    if (selectedCards.cardToNextSeat && selectedCards.cardToPrevSeat) {
      passCards({
        card_to_next_seat: selectedCards.cardToNextSeat,
        card_to_prev_seat: selectedCards.cardToPrevSeat,
      });
      clearSelection();
    }
  };

  // Loading and error states
  if (isLoading) {
    return (
      <div className="min-h-screen game-gradient flex items-center justify-center">
        <div className="text-lg">Loading game...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen game-gradient flex items-center justify-center">
        <div className="text-destructive text-lg">{String(error)}</div>
      </div>
    );
  }

  if (!tableData) {
    return (
      <div className="min-h-screen game-gradient flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  // Extract game state data
  const isGameFinished =
    tableData?.status === "FINISHED" || tableData?.game_state?.is_finished;

  const currentUser = tableData.players?.find((p: any) => p.user_id === userId);
  const currentUserSeat = currentUser?.seat_number;
  const currentPlayerSeatInfo = currentUserSeat
    ? tableData.game_state?.round?.seat_infos?.[currentUserSeat]
    : null;
  const playerHand = currentPlayerSeatInfo?.hand || [];
  const cardsOnBoard = tableData.game_state?.round?.cards_on_board || {};
  const currentPhase = tableData.game_state?.round?.phase || "";

  // Process data
  const processedPlayers = processPlayers(
    tableData.players || [],
    tableData.game_state
  );
  const biddingStatus = extractBiddingStatus(
    tableData.game_state?.round?.seat_infos
  );
  const highestBidInfo = extractHighestBid(
    tableData.game_state?.round?.highest_bid,
    tableData.players || []
  );

  // Check if it's bot's turn
  const activeSeat = tableData.game_state?.active_seat;
  const activePlayer = tableData.players?.find(
    (p: any) => p.seat_number === activeSeat
  );
  const isBotTurn = activePlayer?.bot_strategy_kind;
  const isOwner =
    tableData.owner_id === currentUser?.user_id ||
    tableData.owner_id === currentUser?.id;
  const tableStatus = String(tableData.status || "").toLowerCase();
  const isInProgress = tableStatus === "in_progress";
  const ownerSeatNumber = tableData.players?.find(
    (p: any) => p.user_id === tableData.owner_id
  )?.seat_number;
  const kickableSeatNumbers = isInProgress
    ? (tableData.players || [])
        .filter(
          (p: any) =>
            typeof p.seat_number === "number" &&
            p.seat_number !== ownerSeatNumber
        )
        .map((p: any) => p.seat_number)
    : undefined;

  return (
    <div className="min-h-screen game-gradient">
      <div className="max-w-7xl mx-auto p-4 space-y-4">
        <TableHeader
          wsConnected={wsConnected}
          hasGameState={!!tableData.game_state}
          canJoin={
            isLoggedIn &&
            !tableData.game_state &&
            tableData.players?.length < (tableData.max_players || 3) &&
            !tableData.players.some((p: any) => p.user_id === userId)
          }
          canStartGame={
            isLoggedIn &&
            !tableData.game_state &&
            tableData.players?.length >= (tableData.min_players || 3)
          }
          onJoin={() => join(null)}
          onStartGame={startGame}
          onBack={() => navigate("/tables")}
          isPending={wsPending}
          isAuthenticated={isLoggedIn}
        />

        {isLoggedIn && isOwner && isInProgress && (
          <div className="flex justify-end">
            <Button
              type="button"
              size="sm"
              variant="destructive"
              onClick={handleCancelGame}
              disabled={wsPending}
            >
              {wsPending ? "Cancelling..." : "Cancel Game"}
            </Button>
          </div>
        )}

        <ErrorMessage message={wsError || ""} />

        {isGameFinished && (
          <GameFinishedCard
            gameState={tableData.game_state}
            players={tableData.players || []}
            onStartNewGame={startGame}
            onBackToTables={() => navigate("/tables")}
            isPending={wsPending}
          />
        )}

        {tableData.game_state && (
          <div className="flex flex-col lg:flex-row gap-4 items-stretch w-full min-h-0">
            <div className="flex-1 flex justify-center relative min-w-0 w-full lg:w-auto">
              {isLoggedIn && (
                <>
                  <PassCardsButton
                    cardToNextSeat={selectedCards.cardToNextSeat}
                    cardToPrevSeat={selectedCards.cardToPrevSeat}
                    onPass={handlePassCards}
                    isPending={wsPending}
                  />
                  {tableData.game_state?.round?.phase === "Forming Hands" &&
                    tableData.game_state?.is_my_turn && (
                      <GiveUpButton onGiveUp={giveUp} isPending={wsPending} />
                    )}
                </>
              )}

              <GameBoard
                players={processedPlayers}
                currentUserSeat={currentUserSeat}
                currentUserHand={playerHand}
                selectedCards={
                  [
                    selectedCards.cardToNextSeat,
                    selectedCards.cardToPrevSeat,
                  ].filter(Boolean) as string[]
                }
                hoveredCard={hoveredCard}
                onCardClick={(card) =>
                  handleCardClick(
                    card,
                    currentPhase,
                    tableData.game_state?.is_my_turn || false,
                    (card) => takeTurn({ type: "play_card", params: { card } })
                  )
                }
                onCardHover={setHoveredCard}
                activeSeat={tableData.game_state.active_seat}
                phase={currentPhase}
                cardsOnBoard={cardsOnBoard}
                biddingPanel={
                  isLoggedIn &&
                  tableData.game_state?.is_my_turn &&
                  tableData.game_state?.round?.phase === "Bidding" ? (
                    <BiddingPanel
                      onBid={(amount) =>
                        takeTurn({ type: "make_bid", params: { bid: amount } })
                      }
                      isLoading={wsPending}
                      minBid={60}
                      maxBid={200}
                      hasMarriage={checkForMarriage(playerHand)}
                      currentHighestBid={highestBidInfo?.amount || 0}
                      currentHighestBidder={highestBidInfo?.bidder}
                      biddingStatus={biddingStatus}
                      currentPlayerSeat={currentUserSeat}
                    />
                  ) : null
                }
                playerStats={currentPlayerSeatInfo}
                requiredSuit={tableData.game_state?.round?.required_suit}
                trumpSuit={tableData.game_state?.round?.trump_suit}
                lastTrick={tableData.game_state?.round?.prev_trick}
                highestBid={highestBidInfo}
                canKickPlayers={isLoggedIn && isOwner && isInProgress}
                kickableSeatNumbers={kickableSeatNumbers}
                onKickPlayer={handleAbortPlayer}
                kickDisabled={wsPending}
              />
            </div>

            <div className="lg:hidden">
              {isLoggedIn && isOwner && isBotTurn && (
                <BotTurnButton
                  onTakeTurn={takeAutomaticTurn}
                  isPending={wsPending}
                />
              )}
            </div>

            <div className="hidden lg:block w-full lg:w-64 space-y-4 flex-shrink-0">
              <GameInfoPanel
                phase={currentPhase}
                requiredSuit={tableData.game_state?.round?.required_suit}
                trumpSuit={tableData.game_state?.round?.trump_suit}
                highestBid={tableData.game_state?.round?.highest_bid}
                players={tableData.players || []}
                prevTrick={tableData.game_state?.round?.prev_trick}
              />

              {isLoggedIn && isOwner && isBotTurn && (
                <BotTurnButton
                  onTakeTurn={takeAutomaticTurn}
                  isPending={wsPending}
                />
              )}
            </div>
          </div>
        )}

        <GameStatusCards
          status={tableData.status}
          roundNumber={tableData.game_state?.round?.round_number}
          summary={tableData.game_state?.summary}
          players={tableData.players || []}
        />

        {isLoggedIn &&
          tableData.game_state?.round?.phase === "Forming Hands" &&
          tableData.game_state?.is_my_turn && (
            <CardSelectionInfo
              cardToNextSeat={selectedCards.cardToNextSeat}
              cardToPrevSeat={selectedCards.cardToPrevSeat}
            />
          )}

        {!tableData.game_state && (
          <TableSeats
            players={tableData.players || []}
            userId={userId}
            maxPlayers={tableData.max_players || 3}
            onJoin={join}
            onLeave={leave}
            onAddBot={addBot}
            onRemoveBot={removeBot}
            isPending={wsPending}
            isAuthenticated={isLoggedIn}
          />
        )}

        <details className="mt-4">
          <summary className="cursor-pointer text-sm text-muted-foreground hover:text-foreground">
            View Raw Data (Debug)
          </summary>
          <Card className="mt-2">
            <CardContent className="pt-6">
              <pre className="text-xs overflow-auto max-h-96">
                {JSON.stringify(tableData, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </details>
      </div>
    </div>
  );
}
