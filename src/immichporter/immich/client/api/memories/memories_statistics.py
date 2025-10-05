import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.memory_statistics_response_dto import MemoryStatisticsResponseDto
from ...models.memory_type import MemoryType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    for_: Union[Unset, datetime.datetime] = UNSET,
    is_saved: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    type_: Union[Unset, MemoryType] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_for_: Union[Unset, str] = UNSET
    if not isinstance(for_, Unset):
        json_for_ = for_.isoformat()
    params["for"] = json_for_

    params["isSaved"] = is_saved

    params["isTrashed"] = is_trashed

    json_type_: Union[Unset, str] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/memories/statistics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[MemoryStatisticsResponseDto]:
    if response.status_code == 200:
        response_200 = MemoryStatisticsResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MemoryStatisticsResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    for_: Union[Unset, datetime.datetime] = UNSET,
    is_saved: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    type_: Union[Unset, MemoryType] = UNSET,
) -> Response[MemoryStatisticsResponseDto]:
    """This endpoint requires the `memory.statistics` permission.

    Args:
        for_ (Union[Unset, datetime.datetime]):
        is_saved (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        type_ (Union[Unset, MemoryType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MemoryStatisticsResponseDto]
    """

    kwargs = _get_kwargs(
        for_=for_,
        is_saved=is_saved,
        is_trashed=is_trashed,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    for_: Union[Unset, datetime.datetime] = UNSET,
    is_saved: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    type_: Union[Unset, MemoryType] = UNSET,
) -> Optional[MemoryStatisticsResponseDto]:
    """This endpoint requires the `memory.statistics` permission.

    Args:
        for_ (Union[Unset, datetime.datetime]):
        is_saved (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        type_ (Union[Unset, MemoryType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MemoryStatisticsResponseDto
    """

    return sync_detailed(
        client=client,
        for_=for_,
        is_saved=is_saved,
        is_trashed=is_trashed,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    for_: Union[Unset, datetime.datetime] = UNSET,
    is_saved: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    type_: Union[Unset, MemoryType] = UNSET,
) -> Response[MemoryStatisticsResponseDto]:
    """This endpoint requires the `memory.statistics` permission.

    Args:
        for_ (Union[Unset, datetime.datetime]):
        is_saved (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        type_ (Union[Unset, MemoryType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MemoryStatisticsResponseDto]
    """

    kwargs = _get_kwargs(
        for_=for_,
        is_saved=is_saved,
        is_trashed=is_trashed,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    for_: Union[Unset, datetime.datetime] = UNSET,
    is_saved: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    type_: Union[Unset, MemoryType] = UNSET,
) -> Optional[MemoryStatisticsResponseDto]:
    """This endpoint requires the `memory.statistics` permission.

    Args:
        for_ (Union[Unset, datetime.datetime]):
        is_saved (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        type_ (Union[Unset, MemoryType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MemoryStatisticsResponseDto
    """

    return (
        await asyncio_detailed(
            client=client,
            for_=for_,
            is_saved=is_saved,
            is_trashed=is_trashed,
            type_=type_,
        )
    ).parsed
