from typing import override
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (
    AddBotRequestSerializer,
    CreateGameTableRequestSerializer,
    GameTableWithRelationsSerializer,
    HistoryRequestQuerySerializer,
    JoinGameTableRequestSerializer,
    RemoveBotRequestSerializer,
    TableListRequestQuerySerializer,
    TakeRegularTurnRequestSerializer,
)
from .dependencies import game_table_repository, table_manager


class GameTableViewSet(ViewSet):
    @override
    def get_permissions(self) -> list[BasePermission]:
        if self.action in ["list", "retrieve", "history"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def list(self, request: Request):
        """
        GET /status=not_started,in_progress&game_name=five_hundred
        Query params:
          - status: multiple choice (e.g., status=not_started, in_progress, finished)
          - game_name: multiple choice (e.g., game_name=five_hundred, other_game_name)
        """
        request_serializer = TableListRequestQuerySerializer(data=request.query_params)
        _ = request_serializer.is_valid(raise_exception=True)

        tables = game_table_repository.find_many(filters=request_serializer.validated_data)

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(tables, request)
        response_serializer = GameTableWithRelationsSerializer(page, many=True)
        return paginator.get_paginated_response(response_serializer.data)

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

        table_id = table_manager.add_table(
            raw_config=serializer.validated_data,
            owner_id=request.user.pk,
        )
        headers = {"Location": request.build_absolute_uri(f"{table_id}/")}

        return Response({"table_id": table_id}, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request: Request, pk: str) -> Response:
        """
        DELETE /{table_id}
        """
        table_manager.remove_table(table_id=pk, iniated_by=request.user.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request: Request, pk: str):
        """
        GET /{table_id}
        """
        table = table_manager.get_table(pk)
        user_seat_number: int | None = None
        user_id: int | None = request.user.pk

        for player in table.players:
            if user_id is not None and player.user_id == user_id:
                user_seat_number = player.seat_number
                break
        table_public_dict = table.to_public_dict(user_seat_number)

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

        table = table_manager.join_table(
            table_id=pk,
            user=request.user,
            preferred_seat_number=serializer.validated_data["preferred_seat"],
        )
        headers = {"Location": request.build_absolute_uri(f"{table.id}/")}

        return Response({}, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["post"], url_path="leave")
    def leave(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/leave/
        """
        _ = table_manager.leave_table(table_id=pk, user_id=request.user.pk)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="add-bot")
    def add_bot(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/add-bot/
        {
            "bot_strategy_kind": "random",
            "preferred_seat": 2 // optional
        }
        """
        serializer = AddBotRequestSerializer(data=request.data)
        _ = serializer.is_valid(raise_exception=True)
        _ = table_manager.add_bot_player(
            table_id=pk,
            iniated_by=request.user.pk,
            options=serializer.validated_data,
        )

        return Response({}, status=status.HTTP_201_CREATED)

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
        _ = table_manager.remove_bot_player(
            table_id=pk, iniated_by=request.user.pk, seat_number_to_remove=serializer.validated_data["seat_number"]
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="start-game")
    def start_game(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/start-game/
        """
        _ = table_manager.start_game(table_id=pk, iniated_by=request.user.pk)

        return Response({}, status=status.HTTP_200_OK)

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

        _ = table_manager.take_regular_turn(table_id=pk, user_id=request.user.pk, raw_command=serializer.validated_data)

        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="take-automatic-turn")
    def take_automatic_turn(self, request: Request, pk: str) -> Response:
        """
        POST /{table_id}/take-automatic-turn/
        """
        _ = table_manager.take_automatic_turn(table_id=pk, initiated_by=request.user.pk)

        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request: Request, pk: str) -> Response:
        """
        GET /{table_id}/history?event=100
        """
        serializer = HistoryRequestQuerySerializer(data=request.query_params)
        _ = serializer.is_valid(raise_exception=True)

        table = table_manager.get_table_from_past(table_id=pk, upto_event=serializer.validated_data["event"])
        table_dict = table.to_dict()  # TODO: NOT SAFE during in-progress tables, because contains private info...

        return Response(table_dict, status=status.HTTP_200_OK)
