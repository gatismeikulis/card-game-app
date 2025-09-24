from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    id: str
    # _ws_connection: str # or maybe multiple connections in case player opens game in several tabs or devices...
    # _tables: list[str] # list of tables and user's role at them (player, spectator, etc.)
