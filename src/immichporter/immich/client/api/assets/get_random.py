from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_response_dto import AssetResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    count: Union[Unset, float] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["count"] = count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/assets/random",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["AssetResponseDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AssetResponseDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AssetResponseDto"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    count: Union[Unset, float] = UNSET,
) -> Response[list["AssetResponseDto"]]:
    """This property was deprecated in v1.116.0. This endpoint requires the `asset.read` permission.

    Args:
        count (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AssetResponseDto']]
    """

    kwargs = _get_kwargs(
        count=count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    count: Union[Unset, float] = UNSET,
) -> Optional[list["AssetResponseDto"]]:
    """This property was deprecated in v1.116.0. This endpoint requires the `asset.read` permission.

    Args:
        count (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AssetResponseDto']
    """

    return sync_detailed(
        client=client,
        count=count,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    count: Union[Unset, float] = UNSET,
) -> Response[list["AssetResponseDto"]]:
    """This property was deprecated in v1.116.0. This endpoint requires the `asset.read` permission.

    Args:
        count (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AssetResponseDto']]
    """

    kwargs = _get_kwargs(
        count=count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    count: Union[Unset, float] = UNSET,
) -> Optional[list["AssetResponseDto"]]:
    """This property was deprecated in v1.116.0. This endpoint requires the `asset.read` permission.

    Args:
        count (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AssetResponseDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            count=count,
        )
    ).parsed
