from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.activity_response_dto import ActivityResponseDto
from ...models.reaction_level import ReactionLevel
from ...models.reaction_type import ReactionType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    album_id: UUID,
    asset_id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, ReactionLevel] = UNSET,
    type_: Union[Unset, ReactionType] = UNSET,
    user_id: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_album_id = str(album_id)
    params["albumId"] = json_album_id

    json_asset_id: Union[Unset, str] = UNSET
    if not isinstance(asset_id, Unset):
        json_asset_id = str(asset_id)
    params["assetId"] = json_asset_id

    json_level: Union[Unset, str] = UNSET
    if not isinstance(level, Unset):
        json_level = level.value

    params["level"] = json_level

    json_type_: Union[Unset, str] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    json_user_id: Union[Unset, str] = UNSET
    if not isinstance(user_id, Unset):
        json_user_id = str(user_id)
    params["userId"] = json_user_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/activities",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["ActivityResponseDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ActivityResponseDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ActivityResponseDto"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    album_id: UUID,
    asset_id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, ReactionLevel] = UNSET,
    type_: Union[Unset, ReactionType] = UNSET,
    user_id: Union[Unset, UUID] = UNSET,
) -> Response[list["ActivityResponseDto"]]:
    """This endpoint requires the `activity.read` permission.

    Args:
        album_id (UUID):
        asset_id (Union[Unset, UUID]):
        level (Union[Unset, ReactionLevel]):
        type_ (Union[Unset, ReactionType]):
        user_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ActivityResponseDto']]
    """

    kwargs = _get_kwargs(
        album_id=album_id,
        asset_id=asset_id,
        level=level,
        type_=type_,
        user_id=user_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    album_id: UUID,
    asset_id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, ReactionLevel] = UNSET,
    type_: Union[Unset, ReactionType] = UNSET,
    user_id: Union[Unset, UUID] = UNSET,
) -> Optional[list["ActivityResponseDto"]]:
    """This endpoint requires the `activity.read` permission.

    Args:
        album_id (UUID):
        asset_id (Union[Unset, UUID]):
        level (Union[Unset, ReactionLevel]):
        type_ (Union[Unset, ReactionType]):
        user_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ActivityResponseDto']
    """

    return sync_detailed(
        client=client,
        album_id=album_id,
        asset_id=asset_id,
        level=level,
        type_=type_,
        user_id=user_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    album_id: UUID,
    asset_id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, ReactionLevel] = UNSET,
    type_: Union[Unset, ReactionType] = UNSET,
    user_id: Union[Unset, UUID] = UNSET,
) -> Response[list["ActivityResponseDto"]]:
    """This endpoint requires the `activity.read` permission.

    Args:
        album_id (UUID):
        asset_id (Union[Unset, UUID]):
        level (Union[Unset, ReactionLevel]):
        type_ (Union[Unset, ReactionType]):
        user_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ActivityResponseDto']]
    """

    kwargs = _get_kwargs(
        album_id=album_id,
        asset_id=asset_id,
        level=level,
        type_=type_,
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    album_id: UUID,
    asset_id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, ReactionLevel] = UNSET,
    type_: Union[Unset, ReactionType] = UNSET,
    user_id: Union[Unset, UUID] = UNSET,
) -> Optional[list["ActivityResponseDto"]]:
    """This endpoint requires the `activity.read` permission.

    Args:
        album_id (UUID):
        asset_id (Union[Unset, UUID]):
        level (Union[Unset, ReactionLevel]):
        type_ (Union[Unset, ReactionType]):
        user_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ActivityResponseDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            album_id=album_id,
            asset_id=asset_id,
            level=level,
            type_=type_,
            user_id=user_id,
        )
    ).parsed
