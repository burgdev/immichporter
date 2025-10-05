from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.stack_response_dto import StackResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    primary_asset_id: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_primary_asset_id: Union[Unset, str] = UNSET
    if not isinstance(primary_asset_id, Unset):
        json_primary_asset_id = str(primary_asset_id)
    params["primaryAssetId"] = json_primary_asset_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/stacks",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["StackResponseDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = StackResponseDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["StackResponseDto"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    primary_asset_id: Union[Unset, UUID] = UNSET,
) -> Response[list["StackResponseDto"]]:
    """This endpoint requires the `stack.read` permission.

    Args:
        primary_asset_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['StackResponseDto']]
    """

    kwargs = _get_kwargs(
        primary_asset_id=primary_asset_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    primary_asset_id: Union[Unset, UUID] = UNSET,
) -> Optional[list["StackResponseDto"]]:
    """This endpoint requires the `stack.read` permission.

    Args:
        primary_asset_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['StackResponseDto']
    """

    return sync_detailed(
        client=client,
        primary_asset_id=primary_asset_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    primary_asset_id: Union[Unset, UUID] = UNSET,
) -> Response[list["StackResponseDto"]]:
    """This endpoint requires the `stack.read` permission.

    Args:
        primary_asset_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['StackResponseDto']]
    """

    kwargs = _get_kwargs(
        primary_asset_id=primary_asset_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    primary_asset_id: Union[Unset, UUID] = UNSET,
) -> Optional[list["StackResponseDto"]]:
    """This endpoint requires the `stack.read` permission.

    Args:
        primary_asset_id (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['StackResponseDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            primary_asset_id=primary_asset_id,
        )
    ).parsed
