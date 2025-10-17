from typing import override
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

from .infra.game_play_event_repository import GamePlayEventRepository
from .infra.game_table_repository import GameTableRepository
from .serializers import (
    AddBotRequestSerializer,
    CreateGameTableRequestSerializer,
    GameTableWithRelationsSerializer,
    JoinGameTableRequestSerializer,
    RemoveBotRequestSerializer,
    TakeRegularTurnRequestSerializer,
)
from .application.game_table_manager import GameTableManager


# Creating singletons at module load
_game_table_repository = GameTableRepository()
_game_play_event_repository = GamePlayEventRepository()
_table_manager = GameTableManager(
    game_table_repository=_game_table_repository, game_play_event_repository=_game_play_event_repository
)


# TODO ADD GLOBAL EXCEPTION HANDLER


class GameTableViewSet(ViewSet):
    @override
    def get_permissions(self) -> list[BasePermission]:
        if self.action in ["list", "retrieve", "game_state"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def list(self, request: Request):
        """
        GET /
        Query params:
          - status: comma-separated list (e.g., status=not_started, in_progress, finished)
          - game_name: exact match (e.g., game_name=five_hundred)
          - has_player: player's screen name (case-insensitive)
          - has_user_id: player's user id (pk)
          - game_config_min_players: minimum players from GameConfig(config_key='min_players')
          - table_config_automatic_start: true/false (from TableConfig)
        """
        # TODO extract query params and create filter to pass further to the repository...
        tables = _table_manager.get_tables()
        serializer = GameTableWithRelationsSerializer(tables, many=True)

        return Response({"tables": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        POST /
        {
            "game_name": "five_hundred",
            "game_config": {...}, // optional game-specific config
            "table_config": {...}, // optional table config
        }
        """
        serializer = CreateGameTableRequestSerializer(data=request.data)
        _ = serializer.is_valid(raise_exception=True)

        try:
            table_id = _table_manager.add_table(
                raw_config=serializer.validated_data,
                owner_id=request.user.pk,  # it's always authenticated user because there is IsAuthenticated permission for this action
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        headers = {"Location": request.build_absolute_uri(f"{table_id}/")}

        return Response({"table_id": table_id}, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request: Request, pk: str) -> Response:
        """
        DELETE /{table_id}
        """
        try:
            _ = _table_manager.remove_table(table_id=pk, iniated_by=request.user.pk)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request: Request, pk: str):
        """
        GET /{table_id}
        """
        try:
            table = _table_manager.get_table(pk)
            user_seat_number: int | None = None
            user_id: int | None = request.user.pk

            for player in table.players:
                if user_id is not None and player.user_id == user_id:
                    user_seat_number = player.seat_number
                    break
            table_public_dict = table.to_public_dict(user_seat_number)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        return Response(table_public_dict, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="join")
    def join(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/join/
        {
            "preferred_seat": 2  // optional
        }
        """
        serializer = JoinGameTableRequestSerializer(data=request.data)
        _ = serializer.is_valid(raise_exception=True)
        try:
            table_id = _table_manager.join_table(
                table_id=pk,
                user=request.user,
                preferred_seat_number=serializer.validated_data["preferred_seat"],
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        headers = {"Location": request.build_absolute_uri(f"{table_id}/")}

        return Response({"table_id": table_id}, status=status.HTTP_200_OK, headers=headers)

    @action(detail=True, methods=["post"], url_path="leave")
    def leave(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/leave/
        """
        try:
            _table_manager.leave_table(table_id=pk, user_id=request.user.pk)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="add-bot")
    def add_bot(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/add-bot/
        {
            "bot_strategy_kind": "random",
            "preferred_seat": 2
        }
        """
        serializer = AddBotRequestSerializer(data=request.data)
        _ = serializer.is_valid(raise_exception=True)
        try:
            _table_manager.add_bot_player(
                table_id=pk,
                iniated_by=request.user,
                options=serializer.validated_data,
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="remove-bot")
    def remove_bot(self, request: Request, pk: str) -> Response:
        """
        POST /api/tables/{id}/remove-bot/
        {
            "seat_number": 2
        }
        """
        serializer = RemoveBotRequestSerializer(data=request.data)
        _ = serializer.is_valid(raise_exception=True)
        try:
            _table_manager.remove_bot_player(
                table_id=pk, iniated_by=request.user.pk, seat_number_to_remove=serializer.validated_data["seat_number"]
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="start-game")
    def start_game(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/start-game/
        """
        try:
            _table_manager.start_game(table_id=pk, iniated_by=request.user.pk)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="take-turn")
    def take_regular_turn(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/take-turn/
        {
            "type": "make_bid",
            "params": {...} // command specific data
        }
        """
        serializer = TakeRegularTurnRequestSerializer(data=request.data)
        _ = serializer.is_valid(raise_exception=True)

        try:
            _table_manager.take_regular_turn(
                table_id=pk, user_id=request.user.pk, raw_command=serializer.validated_data
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="take-automatic-turn")
    def take_automatic_turn(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/take-automatic-turn/
        """
        try:
            _table_manager.take_automatic_turn(table_id=pk, iniated_by=request.user.pk)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

        return Response(status=status.HTTP_200_OK)
