from enum import Enum


class TableStatus(Enum):
    NOT_STARTED = "not_started"  # table is created, but game is not started (waiting)
    IN_PROGRESS = "in_progress"  # game is started, but not finished/cancelled/aborted
    FINISHED = "finished"  # game is finished (winners are determined)
    ABORTED = "aborted"  # game is aborted (someone left the table or something unexpected happened)
    CANCELLED = "cancelled"  # table is cancelled, players agreed to cancel the game
