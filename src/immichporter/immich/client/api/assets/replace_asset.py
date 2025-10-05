from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_media_replace_dto import AssetMediaReplaceDto
from ...models.asset_media_response_dto import AssetMediaResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    body: AssetMediaReplaceDto,
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
        "url": "/assets/{id}/original".format(
            id=id,
        ),
        "params": params,
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AssetMediaResponseDto]:
    if response.status_code == 200:
        response_200 = AssetMediaResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AssetMediaResponseDto]:
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
    body: AssetMediaReplaceDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Response[AssetMediaResponseDto]:
    """Replace the asset with new file, without changing its id

     This property was deprecated in v1.142.0. Replace the asset with new file, without changing its id.
    This endpoint requires the `asset.replace` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (AssetMediaReplaceDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetMediaResponseDto]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
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
    body: AssetMediaReplaceDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Optional[AssetMediaResponseDto]:
    """Replace the asset with new file, without changing its id

     This property was deprecated in v1.142.0. Replace the asset with new file, without changing its id.
    This endpoint requires the `asset.replace` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (AssetMediaReplaceDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetMediaResponseDto
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        key=key,
        slug=slug,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: AssetMediaReplaceDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Response[AssetMediaResponseDto]:
    """Replace the asset with new file, without changing its id

     This property was deprecated in v1.142.0. Replace the asset with new file, without changing its id.
    This endpoint requires the `asset.replace` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (AssetMediaReplaceDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetMediaResponseDto]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        key=key,
        slug=slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: AssetMediaReplaceDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Optional[AssetMediaResponseDto]:
    """Replace the asset with new file, without changing its id

     This property was deprecated in v1.142.0. Replace the asset with new file, without changing its id.
    This endpoint requires the `asset.replace` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (AssetMediaReplaceDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetMediaResponseDto
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            key=key,
            slug=slug,
        )
    ).parsed
