from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GameTableConfig:
    min_players: int
    max_players: int
    automatic_start: bool
