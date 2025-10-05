from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.notification_dto import NotificationDto
from ...models.notification_level import NotificationLevel
from ...models.notification_type import NotificationType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, NotificationLevel] = UNSET,
    type_: Union[Unset, NotificationType] = UNSET,
    unread: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_id: Union[Unset, str] = UNSET
    if not isinstance(id, Unset):
        json_id = str(id)
    params["id"] = json_id

    json_level: Union[Unset, str] = UNSET
    if not isinstance(level, Unset):
        json_level = level.value

    params["level"] = json_level

    json_type_: Union[Unset, str] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params["unread"] = unread

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/notifications",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["NotificationDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = NotificationDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["NotificationDto"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, NotificationLevel] = UNSET,
    type_: Union[Unset, NotificationType] = UNSET,
    unread: Union[Unset, bool] = UNSET,
) -> Response[list["NotificationDto"]]:
    """This endpoint requires the `notification.read` permission.

    Args:
        id (Union[Unset, UUID]):
        level (Union[Unset, NotificationLevel]):
        type_ (Union[Unset, NotificationType]):
        unread (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['NotificationDto']]
    """

    kwargs = _get_kwargs(
        id=id,
        level=level,
        type_=type_,
        unread=unread,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, NotificationLevel] = UNSET,
    type_: Union[Unset, NotificationType] = UNSET,
    unread: Union[Unset, bool] = UNSET,
) -> Optional[list["NotificationDto"]]:
    """This endpoint requires the `notification.read` permission.

    Args:
        id (Union[Unset, UUID]):
        level (Union[Unset, NotificationLevel]):
        type_ (Union[Unset, NotificationType]):
        unread (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['NotificationDto']
    """

    return sync_detailed(
        client=client,
        id=id,
        level=level,
        type_=type_,
        unread=unread,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, NotificationLevel] = UNSET,
    type_: Union[Unset, NotificationType] = UNSET,
    unread: Union[Unset, bool] = UNSET,
) -> Response[list["NotificationDto"]]:
    """This endpoint requires the `notification.read` permission.

    Args:
        id (Union[Unset, UUID]):
        level (Union[Unset, NotificationLevel]):
        type_ (Union[Unset, NotificationType]):
        unread (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['NotificationDto']]
    """

    kwargs = _get_kwargs(
        id=id,
        level=level,
        type_=type_,
        unread=unread,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id: Union[Unset, UUID] = UNSET,
    level: Union[Unset, NotificationLevel] = UNSET,
    type_: Union[Unset, NotificationType] = UNSET,
    unread: Union[Unset, bool] = UNSET,
) -> Optional[list["NotificationDto"]]:
    """This endpoint requires the `notification.read` permission.

    Args:
        id (Union[Unset, UUID]):
        level (Union[Unset, NotificationLevel]):
        type_ (Union[Unset, NotificationType]):
        unread (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['NotificationDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            level=level,
            type_=type_,
            unread=unread,
        )
    ).parsed
