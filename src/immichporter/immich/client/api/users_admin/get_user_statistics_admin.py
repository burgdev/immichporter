from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_stats_response_dto import AssetStatsResponseDto
from ...models.asset_visibility import AssetVisibility
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["isFavorite"] = is_favorite

    params["isTrashed"] = is_trashed

    json_visibility: Union[Unset, str] = UNSET
    if not isinstance(visibility, Unset):
        json_visibility = visibility.value

    params["visibility"] = json_visibility

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/users/{id}/statistics".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AssetStatsResponseDto]:
    if response.status_code == 200:
        response_200 = AssetStatsResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AssetStatsResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
) -> Response[AssetStatsResponseDto]:
    """This endpoint is an admin-only route, and requires the `adminUser.read` permission.

    Args:
        id (UUID):
        is_favorite (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        visibility (Union[Unset, AssetVisibility]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetStatsResponseDto]
    """

    kwargs = _get_kwargs(
        id=id,
        is_favorite=is_favorite,
        is_trashed=is_trashed,
        visibility=visibility,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
) -> Optional[AssetStatsResponseDto]:
    """This endpoint is an admin-only route, and requires the `adminUser.read` permission.

    Args:
        id (UUID):
        is_favorite (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        visibility (Union[Unset, AssetVisibility]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetStatsResponseDto
    """

    return sync_detailed(
        id=id,
        client=client,
        is_favorite=is_favorite,
        is_trashed=is_trashed,
        visibility=visibility,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
) -> Response[AssetStatsResponseDto]:
    """This endpoint is an admin-only route, and requires the `adminUser.read` permission.

    Args:
        id (UUID):
        is_favorite (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        visibility (Union[Unset, AssetVisibility]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetStatsResponseDto]
    """

    kwargs = _get_kwargs(
        id=id,
        is_favorite=is_favorite,
        is_trashed=is_trashed,
        visibility=visibility,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
) -> Optional[AssetStatsResponseDto]:
    """This endpoint is an admin-only route, and requires the `adminUser.read` permission.

    Args:
        id (UUID):
        is_favorite (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        visibility (Union[Unset, AssetVisibility]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetStatsResponseDto
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            is_favorite=is_favorite,
            is_trashed=is_trashed,
            visibility=visibility,
        )
    ).parsed
