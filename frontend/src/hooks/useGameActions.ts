import { useCallback } from "react";

interface UseGameActionsProps {
  sendMessage: (action: string, data: any) => void;
}

export function useGameActions({ sendMessage }: UseGameActionsProps) {
  const join = useCallback(
    (preferredSeat: number | null = null) => {
      sendMessage("JOIN_TABLE", { preferred_seat: preferredSeat });
    },
    [sendMessage]
  );

  const leave = useCallback(() => {
    sendMessage("LEAVE_TABLE", {});
  }, [sendMessage]);

  const addBot = useCallback(
    (seatNumber: number) => {
      sendMessage("ADD_BOT", {
        bot_strategy_kind: "random",
        preferred_seat: seatNumber,
      });
    },
    [sendMessage]
  );

  const removeBot = useCallback(
    (seatNumber: number) => {
      sendMessage("REMOVE_BOT", { seat_number: seatNumber });
    },
    [sendMessage]
  );

  const startGame = useCallback(() => {
    sendMessage("START_GAME", {});
  }, [sendMessage]);

  const takeTurn = useCallback(
    (command: { type: string; params: any }) => {
      sendMessage("TAKE_REGULAR_TURN", command);
    },
    [sendMessage]
  );

  const takeAutomaticTurn = useCallback(() => {
    sendMessage("TAKE_AUTOMATIC_TURN", {});
  }, [sendMessage]);

  const passCards = useCallback(
    (cards: { card_to_next_seat: string; card_to_prev_seat: string }) => {
      sendMessage("TAKE_REGULAR_TURN", {
        type: "pass_cards",
        params: cards,
      });
    },
    [sendMessage]
  );

  const giveUp = useCallback(() => {
    sendMessage("TAKE_REGULAR_TURN", {
      type: "give_up",
      params: {},
    });
  }, [sendMessage]);

  const cancelGame = useCallback(() => {
    sendMessage("CANCEL_GAME", {
      type: "end_game",
      params: {
        reason: "CANCELLED",
        seat: null,
      },
    });
  }, [sendMessage]);

  const abortGame = useCallback(
    (seatNumber: number) => {
      sendMessage("ABORT_GAME", {
        type: "end_game",
        params: {
          reason: "ABORTED",
          seat: seatNumber,
        },
        to_blame: seatNumber,
      });
    },
    [sendMessage]
  );

  return {
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
  };
}

