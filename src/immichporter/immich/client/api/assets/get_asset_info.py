from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_response_dto import AssetResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["key"] = key

    params["slug"] = slug

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/assets/{id}".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AssetResponseDto]:
    if response.status_code == 200:
        response_200 = AssetResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AssetResponseDto]:
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
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Response[AssetResponseDto]:
    """This endpoint requires the `asset.read` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetResponseDto]
    """

    kwargs = _get_kwargs(
        id=id,
        key=key,
        slug=slug,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Optional[AssetResponseDto]:
    """This endpoint requires the `asset.read` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetResponseDto
    """

    return sync_detailed(
        id=id,
        client=client,
        key=key,
        slug=slug,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Response[AssetResponseDto]:
    """This endpoint requires the `asset.read` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetResponseDto]
    """

    kwargs = _get_kwargs(
        id=id,
        key=key,
        slug=slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Optional[AssetResponseDto]:
    """This endpoint requires the `asset.read` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetResponseDto
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            key=key,
            slug=slug,
        )
    ).parsed
