from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.albums_add_assets_dto import AlbumsAddAssetsDto
from ...models.albums_add_assets_response_dto import AlbumsAddAssetsResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AlbumsAddAssetsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["key"] = key

    params["slug"] = slug

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/albums/assets",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AlbumsAddAssetsResponseDto]:
    if response.status_code == 200:
        response_200 = AlbumsAddAssetsResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AlbumsAddAssetsResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AlbumsAddAssetsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Response[AlbumsAddAssetsResponseDto]:
    """This endpoint requires the `albumAsset.create` permission.

    Args:
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (AlbumsAddAssetsDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AlbumsAddAssetsResponseDto]
    """

    kwargs = _get_kwargs(
        body=body,
        key=key,
        slug=slug,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: AlbumsAddAssetsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Optional[AlbumsAddAssetsResponseDto]:
    """This endpoint requires the `albumAsset.create` permission.

    Args:
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (AlbumsAddAssetsDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AlbumsAddAssetsResponseDto
    """

    return sync_detailed(
        client=client,
        body=body,
        key=key,
        slug=slug,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AlbumsAddAssetsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Response[AlbumsAddAssetsResponseDto]:
    """This endpoint requires the `albumAsset.create` permission.

    Args:
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (AlbumsAddAssetsDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AlbumsAddAssetsResponseDto]
    """

    kwargs = _get_kwargs(
        body=body,
        key=key,
        slug=slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AlbumsAddAssetsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Optional[AlbumsAddAssetsResponseDto]:
    """This endpoint requires the `albumAsset.create` permission.

    Args:
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (AlbumsAddAssetsDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AlbumsAddAssetsResponseDto
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            key=key,
            slug=slug,
        )
    ).parsed
