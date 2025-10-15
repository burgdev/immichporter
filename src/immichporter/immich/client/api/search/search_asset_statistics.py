from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_statistics_response_dto import SearchStatisticsResponseDto
from ...models.statistics_search_dto import StatisticsSearchDto
from ...types import Response


def _get_kwargs(
    *,
    body: StatisticsSearchDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/search/statistics",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SearchStatisticsResponseDto]:
    if response.status_code == 200:
        response_200 = SearchStatisticsResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SearchStatisticsResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: StatisticsSearchDto,
) -> Response[SearchStatisticsResponseDto]:
    """This endpoint requires the `asset.statistics` permission.

    Args:
        body (StatisticsSearchDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchStatisticsResponseDto]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: StatisticsSearchDto,
) -> Optional[SearchStatisticsResponseDto]:
    """This endpoint requires the `asset.statistics` permission.

    Args:
        body (StatisticsSearchDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchStatisticsResponseDto
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: StatisticsSearchDto,
) -> Response[SearchStatisticsResponseDto]:
    """This endpoint requires the `asset.statistics` permission.

    Args:
        body (StatisticsSearchDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchStatisticsResponseDto]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: StatisticsSearchDto,
) -> Optional[SearchStatisticsResponseDto]:
    """This endpoint requires the `asset.statistics` permission.

    Args:
        body (StatisticsSearchDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchStatisticsResponseDto
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
