from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.partner_direction import PartnerDirection
from ...models.partner_response_dto import PartnerResponseDto
from ...types import UNSET, Response


def _get_kwargs(
    *,
    direction: PartnerDirection,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_direction = direction.value
    params["direction"] = json_direction

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/partners",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["PartnerResponseDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PartnerResponseDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PartnerResponseDto"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    direction: PartnerDirection,
) -> Response[list["PartnerResponseDto"]]:
    """This endpoint requires the `partner.read` permission.

    Args:
        direction (PartnerDirection):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PartnerResponseDto']]
    """

    kwargs = _get_kwargs(
        direction=direction,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    direction: PartnerDirection,
) -> Optional[list["PartnerResponseDto"]]:
    """This endpoint requires the `partner.read` permission.

    Args:
        direction (PartnerDirection):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PartnerResponseDto']
    """

    return sync_detailed(
        client=client,
        direction=direction,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    direction: PartnerDirection,
) -> Response[list["PartnerResponseDto"]]:
    """This endpoint requires the `partner.read` permission.

    Args:
        direction (PartnerDirection):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PartnerResponseDto']]
    """

    kwargs = _get_kwargs(
        direction=direction,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    direction: PartnerDirection,
) -> Optional[list["PartnerResponseDto"]]:
    """This endpoint requires the `partner.read` permission.

    Args:
        direction (PartnerDirection):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PartnerResponseDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            direction=direction,
        )
    ).parsed
