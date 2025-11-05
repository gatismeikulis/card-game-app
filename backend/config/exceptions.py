from typing import Any
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from apps.gametables.exceptions import GameTableInternalException
from game.common.game_exception import GameEngineException, GameParsingException
from core.exceptions.app_exception import AppException
from core.exceptions.domain_exception import DomainException
from core.exceptions.not_exist_exception import NotExistException


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    response = exception_handler(exc, context)

    if response is not None:
        return response

    print(f"EXCEPTION: {exc}")

    if isinstance(exc, AppException):
        match exc:
            case DomainException() as domain_exception:
                match domain_exception:
                    case GameParsingException():
                        status_code = status.HTTP_400_BAD_REQUEST
                    case GameEngineException():
                        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                    case GameTableInternalException():
                        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                    case _:
                        status_code = status.HTTP_400_BAD_REQUEST
            case NotExistException():
                status_code = status.HTTP_404_NOT_FOUND
            case _:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(exc.to_dict_minimal(), status=status_code)

    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
