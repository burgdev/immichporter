from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.shared_link_response_dto import SharedLinkResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    album_id: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_album_id: Union[Unset, str] = UNSET
    if not isinstance(album_id, Unset):
        json_album_id = str(album_id)
    params["albumId"] = json_album_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/shared-links",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["SharedLinkResponseDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SharedLinkResponseDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["SharedLinkResponseDto"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    album_id: Union[Unset, UUID] = UNSET,
) -> Response[list["SharedLinkResponseDto"]]:
    """This endpoint requires the `sharedLink.read` permission.

    Args:
        album_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SharedLinkResponseDto']]
    """

    kwargs = _get_kwargs(
        album_id=album_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    album_id: Union[Unset, UUID] = UNSET,
) -> Optional[list["SharedLinkResponseDto"]]:
    """This endpoint requires the `sharedLink.read` permission.

    Args:
        album_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SharedLinkResponseDto']
    """

    return sync_detailed(
        client=client,
        album_id=album_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    album_id: Union[Unset, UUID] = UNSET,
) -> Response[list["SharedLinkResponseDto"]]:
    """This endpoint requires the `sharedLink.read` permission.

    Args:
        album_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SharedLinkResponseDto']]
    """

    kwargs = _get_kwargs(
        album_id=album_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    album_id: Union[Unset, UUID] = UNSET,
) -> Optional[list["SharedLinkResponseDto"]]:
    """This endpoint requires the `sharedLink.read` permission.

    Args:
        album_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SharedLinkResponseDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            album_id=album_id,
        )
    ).parsed
