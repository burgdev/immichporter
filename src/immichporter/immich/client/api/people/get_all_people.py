from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.people_response_dto import PeopleResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    closest_asset_id: Union[Unset, UUID] = UNSET,
    closest_person_id: Union[Unset, UUID] = UNSET,
    page: Union[Unset, float] = 1.0,
    size: Union[Unset, float] = 500.0,
    with_hidden: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_closest_asset_id: Union[Unset, str] = UNSET
    if not isinstance(closest_asset_id, Unset):
        json_closest_asset_id = str(closest_asset_id)
    params["closestAssetId"] = json_closest_asset_id

    json_closest_person_id: Union[Unset, str] = UNSET
    if not isinstance(closest_person_id, Unset):
        json_closest_person_id = str(closest_person_id)
    params["closestPersonId"] = json_closest_person_id

    params["page"] = page

    params["size"] = size

    params["withHidden"] = with_hidden

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/people",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PeopleResponseDto]:
    if response.status_code == 200:
        response_200 = PeopleResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PeopleResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    closest_asset_id: Union[Unset, UUID] = UNSET,
    closest_person_id: Union[Unset, UUID] = UNSET,
    page: Union[Unset, float] = 1.0,
    size: Union[Unset, float] = 500.0,
    with_hidden: Union[Unset, bool] = UNSET,
) -> Response[PeopleResponseDto]:
    """This endpoint requires the `person.read` permission.

    Args:
        closest_asset_id (Union[Unset, UUID]):
        closest_person_id (Union[Unset, UUID]):
        page (Union[Unset, float]):  Default: 1.0.
        size (Union[Unset, float]):  Default: 500.0.
        with_hidden (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PeopleResponseDto]
    """

    kwargs = _get_kwargs(
        closest_asset_id=closest_asset_id,
        closest_person_id=closest_person_id,
        page=page,
        size=size,
        with_hidden=with_hidden,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    closest_asset_id: Union[Unset, UUID] = UNSET,
    closest_person_id: Union[Unset, UUID] = UNSET,
    page: Union[Unset, float] = 1.0,
    size: Union[Unset, float] = 500.0,
    with_hidden: Union[Unset, bool] = UNSET,
) -> Optional[PeopleResponseDto]:
    """This endpoint requires the `person.read` permission.

    Args:
        closest_asset_id (Union[Unset, UUID]):
        closest_person_id (Union[Unset, UUID]):
        page (Union[Unset, float]):  Default: 1.0.
        size (Union[Unset, float]):  Default: 500.0.
        with_hidden (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PeopleResponseDto
    """

    return sync_detailed(
        client=client,
        closest_asset_id=closest_asset_id,
        closest_person_id=closest_person_id,
        page=page,
        size=size,
        with_hidden=with_hidden,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    closest_asset_id: Union[Unset, UUID] = UNSET,
    closest_person_id: Union[Unset, UUID] = UNSET,
    page: Union[Unset, float] = 1.0,
    size: Union[Unset, float] = 500.0,
    with_hidden: Union[Unset, bool] = UNSET,
) -> Response[PeopleResponseDto]:
    """This endpoint requires the `person.read` permission.

    Args:
        closest_asset_id (Union[Unset, UUID]):
        closest_person_id (Union[Unset, UUID]):
        page (Union[Unset, float]):  Default: 1.0.
        size (Union[Unset, float]):  Default: 500.0.
        with_hidden (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PeopleResponseDto]
    """

    kwargs = _get_kwargs(
        closest_asset_id=closest_asset_id,
        closest_person_id=closest_person_id,
        page=page,
        size=size,
        with_hidden=with_hidden,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    closest_asset_id: Union[Unset, UUID] = UNSET,
    closest_person_id: Union[Unset, UUID] = UNSET,
    page: Union[Unset, float] = 1.0,
    size: Union[Unset, float] = 500.0,
    with_hidden: Union[Unset, bool] = UNSET,
) -> Optional[PeopleResponseDto]:
    """This endpoint requires the `person.read` permission.

    Args:
        closest_asset_id (Union[Unset, UUID]):
        closest_person_id (Union[Unset, UUID]):
        page (Union[Unset, float]):  Default: 1.0.
        size (Union[Unset, float]):  Default: 500.0.
        with_hidden (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PeopleResponseDto
    """

    return (
        await asyncio_detailed(
            client=client,
            closest_asset_id=closest_asset_id,
            closest_person_id=closest_person_id,
            page=page,
            size=size,
            with_hidden=with_hidden,
        )
    ).parsed
