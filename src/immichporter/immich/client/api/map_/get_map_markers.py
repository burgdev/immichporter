import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.map_marker_response_dto import MapMarkerResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    is_archived: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    file_created_after: Union[Unset, datetime.datetime] = UNSET,
    file_created_before: Union[Unset, datetime.datetime] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_shared_albums: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["isArchived"] = is_archived

    params["isFavorite"] = is_favorite

    json_file_created_after: Union[Unset, str] = UNSET
    if not isinstance(file_created_after, Unset):
        json_file_created_after = file_created_after.isoformat()
    params["fileCreatedAfter"] = json_file_created_after

    json_file_created_before: Union[Unset, str] = UNSET
    if not isinstance(file_created_before, Unset):
        json_file_created_before = file_created_before.isoformat()
    params["fileCreatedBefore"] = json_file_created_before

    params["withPartners"] = with_partners

    params["withSharedAlbums"] = with_shared_albums

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/map/markers",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["MapMarkerResponseDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MapMarkerResponseDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["MapMarkerResponseDto"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    is_archived: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    file_created_after: Union[Unset, datetime.datetime] = UNSET,
    file_created_before: Union[Unset, datetime.datetime] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_shared_albums: Union[Unset, bool] = UNSET,
) -> Response[list["MapMarkerResponseDto"]]:
    """
    Args:
        is_archived (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        file_created_after (Union[Unset, datetime.datetime]):
        file_created_before (Union[Unset, datetime.datetime]):
        with_partners (Union[Unset, bool]):
        with_shared_albums (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MapMarkerResponseDto']]
    """

    kwargs = _get_kwargs(
        is_archived=is_archived,
        is_favorite=is_favorite,
        file_created_after=file_created_after,
        file_created_before=file_created_before,
        with_partners=with_partners,
        with_shared_albums=with_shared_albums,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    is_archived: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    file_created_after: Union[Unset, datetime.datetime] = UNSET,
    file_created_before: Union[Unset, datetime.datetime] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_shared_albums: Union[Unset, bool] = UNSET,
) -> Optional[list["MapMarkerResponseDto"]]:
    """
    Args:
        is_archived (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        file_created_after (Union[Unset, datetime.datetime]):
        file_created_before (Union[Unset, datetime.datetime]):
        with_partners (Union[Unset, bool]):
        with_shared_albums (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MapMarkerResponseDto']
    """

    return sync_detailed(
        client=client,
        is_archived=is_archived,
        is_favorite=is_favorite,
        file_created_after=file_created_after,
        file_created_before=file_created_before,
        with_partners=with_partners,
        with_shared_albums=with_shared_albums,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    is_archived: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    file_created_after: Union[Unset, datetime.datetime] = UNSET,
    file_created_before: Union[Unset, datetime.datetime] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_shared_albums: Union[Unset, bool] = UNSET,
) -> Response[list["MapMarkerResponseDto"]]:
    """
    Args:
        is_archived (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        file_created_after (Union[Unset, datetime.datetime]):
        file_created_before (Union[Unset, datetime.datetime]):
        with_partners (Union[Unset, bool]):
        with_shared_albums (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MapMarkerResponseDto']]
    """

    kwargs = _get_kwargs(
        is_archived=is_archived,
        is_favorite=is_favorite,
        file_created_after=file_created_after,
        file_created_before=file_created_before,
        with_partners=with_partners,
        with_shared_albums=with_shared_albums,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    is_archived: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    file_created_after: Union[Unset, datetime.datetime] = UNSET,
    file_created_before: Union[Unset, datetime.datetime] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_shared_albums: Union[Unset, bool] = UNSET,
) -> Optional[list["MapMarkerResponseDto"]]:
    """
    Args:
        is_archived (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        file_created_after (Union[Unset, datetime.datetime]):
        file_created_before (Union[Unset, datetime.datetime]):
        with_partners (Union[Unset, bool]):
        with_shared_albums (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MapMarkerResponseDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            is_archived=is_archived,
            is_favorite=is_favorite,
            file_created_after=file_created_after,
            file_created_before=file_created_before,
            with_partners=with_partners,
            with_shared_albums=with_shared_albums,
        )
    ).parsed
