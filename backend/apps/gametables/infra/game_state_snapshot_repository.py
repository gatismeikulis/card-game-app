from collections.abc import Sequence
import json
from typing import Any, override
from redis import Redis

from ..application.igame_state_snapshot_repository import IGameStateSnapshotRepository


class GameStateSnapshotRepository(IGameStateSnapshotRepository):
    def __init__(self, redis_conn: Redis):
        self.redis: Redis = redis_conn
        self.prefix: str = "game_state_snapshot"
        self.ttl_in_seconds: int = 60 * 60 * 6  # 6 hours

    def _make_key(self, table_id: str, turn_number: int, event_number: int) -> str:
        return f"{self.prefix}:{table_id}:{turn_number}:{event_number}"

    @override
    def get(self, table_id: str, turn_number: int | None, event_number: int | None) -> dict[str, Any] | None:
        sets = [f"index:table_id:{table_id}"]

        if turn_number is not None:
            sets.append(f"index:turn_number:{turn_number}")
        elif event_number is not None:
            sets.append(f"index:event_number:{event_number}")
        else:
            sets.append("index:event_number:0")

        # Get intersection of all sets (keys that match all criteria)
        keys = self.redis.sinter(*sets)

        if not keys or len(keys) == 0:
            return None

        key = keys.pop()  # TODO: fix this because this can return different snapshot if searched by turn_number (pop returns random element from set)

        # if isinstance(key, bytes):
        #     key = key.decode()
        # elif not isinstance(key, str):
        #     key = str(key)

        print("key: ", key)

        snapshot = self.redis.get(key)

        return json.loads(snapshot) if snapshot else None

    @override
    def store(self, snapshots: Sequence[dict[str, Any]]) -> None:
        if not snapshots:
            return

        # batch mode
        with self.redis.pipeline(transaction=False) as pipe:
            for snap in snapshots:
                key = self._make_key(snap["table_id"], snap["turn_number"], snap["event_number"])
                _ = self.redis.set(key, json.dumps(snap["payload"]), ex=self.ttl_in_seconds)
                _ = pipe.sadd(f"index:table_id:{snap['table_id']}", key)
                _ = pipe.sadd(f"index:turn_number:{snap['turn_number']}", key)
                _ = pipe.sadd(f"index:event_number:{snap['event_number']}", key)

            _ = pipe.execute()
