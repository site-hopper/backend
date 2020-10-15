from typing import Callable, Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from firebase_admin import auth
from users.models import User
from resources import strings

HEADER_KEY = "Authorization"


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(  # noqa: WPS610
            self,
            request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=strings.AUTHENTICATION_REQUIRED,
            )


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_user if required else _get_current_user_optional


def _get_authorization_header_retriever(
        *,
        required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


def _get_authorization_header(
        api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )
    return token


def _get_authorization_header_optional(
        authorization: Optional[str] = Security(
            RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
        ),
) -> str:
    if authorization:
        return _get_authorization_header(authorization)

    return ""


async def _get_current_user(
        token: str = Depends(_get_authorization_header_retriever()),
) -> User:
    try:
        username_id = get_uid_from_token(token)
        return User(username_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )


async def _get_current_user_optional(
        token: str = Depends(_get_authorization_header_retriever(required=False)),
) -> Optional[User]:
    if token:
        return await _get_current_user(token)

    return None


def get_uid_from_token(id_token: str):
    result = auth.verify_id_token(id_token)
    print(result)
    return result.get("uid", None)
