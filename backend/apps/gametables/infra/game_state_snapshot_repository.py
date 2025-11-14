from collections.abc import Mapping, Sequence
import json
import logging
from typing import Any, override
from redis import Redis

from core.exceptions.infrastructure_exception import InfrastructureException
from ..application.igame_state_snapshot_repository import IGameStateSnapshotRepository

logger = logging.getLogger(__name__)


class GameStateSnapshotRepository(IGameStateSnapshotRepository):
    def __init__(self, redis_conn: Redis):
        self.redis: Redis = redis_conn
        self.prefix: str = "game_state_snapshot"
        self.ttl_in_seconds: int = 60 * 60 * 6  # 6 hours

    def _make_key(self, table_id: str, event_number: int) -> str:
        return f"{self.prefix}:{table_id}:{event_number}"

    @override
    def get_exact_or_nearest_snapshot_data(self, table_id: str, event_number: int = 0) -> Mapping[str, Any] | None:
        try:
            # attempt to get exact snapshot
            exact_key = self._make_key(table_id, event_number)
            raw_exact_snapshot = self.redis.get(exact_key)

            if raw_exact_snapshot:
                return {
                    "is_exact": True,
                    "snapshot": json.loads(raw_exact_snapshot),
                }

            # attempt to find a key for neareast snapshot to the desired one
            zset_key = f"index:zset:table_id:{table_id}"
            nearest_keys = self.redis.zrevrangebyscore(name=zset_key, max=event_number, min="-inf", start=0, num=1)

            if not nearest_keys:
                return None

            nearest_key = nearest_keys[0].decode() if isinstance(nearest_keys[0], bytes) else nearest_keys[0]
            raw_nearest_snapshot = self.redis.get(nearest_key)

            if not raw_nearest_snapshot:
                logger.error(f"Could not find game_state snapshot for table {table_id} and event number {event_number}")
                return None

            return {"is_exact": False, "snapshot": json.loads(raw_nearest_snapshot)}

        except Exception as e:
            logger.error(f"Unexpected error getting snapshot for table {table_id}, event {event_number}", exc_info=True)
            raise InfrastructureException(detail=f"Unexpected error: {e}", reason="unexpected_error") from e

    @override
    def store(self, table_id: str, raw_snapshots: Sequence[dict[str, Any]]) -> None:
        if not raw_snapshots:
            return

        # batch mode
        try:
            with self.redis.pipeline(transaction=False) as pipe:
                for data in raw_snapshots:
                    key = self._make_key(table_id, event_number=data["event_number"])
                    _ = pipe.set(key, json.dumps(data), ex=self.ttl_in_seconds)

                    # add zset index so we can find the nearest snapshot to desired one by event_number
                    zset_key = f"index:zset:table_id:{table_id}"
                    _ = pipe.zadd(zset_key, {key: data["event_number"]})
                    _ = pipe.expire(zset_key, self.ttl_in_seconds)

                _ = pipe.execute()
        except Exception as e:
            logger.error(f"Unexpected error storing snapshots for table {table_id}", exc_info=True)
            raise InfrastructureException(detail=f"Unexpected error: {e}", reason="unexpected_error") from e
