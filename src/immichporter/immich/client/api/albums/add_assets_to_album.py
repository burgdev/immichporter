from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_id_response_dto import BulkIdResponseDto
from ...models.bulk_ids_dto import BulkIdsDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    body: BulkIdsDto,
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
        "url": "/albums/{id}/assets".format(
            id=id,
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["BulkIdResponseDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = BulkIdResponseDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["BulkIdResponseDto"]]:
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
    body: BulkIdsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Response[list["BulkIdResponseDto"]]:
    """This endpoint requires the `albumAsset.create` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (BulkIdsDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['BulkIdResponseDto']]
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
    body: BulkIdsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Optional[list["BulkIdResponseDto"]]:
    """This endpoint requires the `albumAsset.create` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (BulkIdsDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BulkIdResponseDto']
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
    body: BulkIdsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Response[list["BulkIdResponseDto"]]:
    """This endpoint requires the `albumAsset.create` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (BulkIdsDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['BulkIdResponseDto']]
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
    body: BulkIdsDto,
    key: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
) -> Optional[list["BulkIdResponseDto"]]:
    """This endpoint requires the `albumAsset.create` permission.

    Args:
        id (UUID):
        key (Union[Unset, str]):
        slug (Union[Unset, str]):
        body (BulkIdsDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BulkIdResponseDto']
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
