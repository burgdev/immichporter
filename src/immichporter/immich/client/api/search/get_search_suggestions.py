from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_suggestion_type import SearchSuggestionType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    country: Union[Unset, str] = UNSET,
    include_null: Union[Unset, bool] = UNSET,
    make: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    type_: SearchSuggestionType,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["country"] = country

    params["includeNull"] = include_null

    params["make"] = make

    params["model"] = model

    params["state"] = state

    json_type_ = type_.value
    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/search/suggestions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list[str]]:
    if response.status_code == 200:
        response_200 = cast(list[str], response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list[str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    include_null: Union[Unset, bool] = UNSET,
    make: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    type_: SearchSuggestionType,
) -> Response[list[str]]:
    """This endpoint requires the `asset.read` permission.

    Args:
        country (Union[Unset, str]):
        include_null (Union[Unset, bool]):
        make (Union[Unset, str]):
        model (Union[Unset, str]):
        state (Union[Unset, str]):
        type_ (SearchSuggestionType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[str]]
    """

    kwargs = _get_kwargs(
        country=country,
        include_null=include_null,
        make=make,
        model=model,
        state=state,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    include_null: Union[Unset, bool] = UNSET,
    make: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    type_: SearchSuggestionType,
) -> Optional[list[str]]:
    """This endpoint requires the `asset.read` permission.

    Args:
        country (Union[Unset, str]):
        include_null (Union[Unset, bool]):
        make (Union[Unset, str]):
        model (Union[Unset, str]):
        state (Union[Unset, str]):
        type_ (SearchSuggestionType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[str]
    """

    return sync_detailed(
        client=client,
        country=country,
        include_null=include_null,
        make=make,
        model=model,
        state=state,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    include_null: Union[Unset, bool] = UNSET,
    make: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    type_: SearchSuggestionType,
) -> Response[list[str]]:
    """This endpoint requires the `asset.read` permission.

    Args:
        country (Union[Unset, str]):
        include_null (Union[Unset, bool]):
        make (Union[Unset, str]):
        model (Union[Unset, str]):
        state (Union[Unset, str]):
        type_ (SearchSuggestionType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[str]]
    """

    kwargs = _get_kwargs(
        country=country,
        include_null=include_null,
        make=make,
        model=model,
        state=state,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    include_null: Union[Unset, bool] = UNSET,
    make: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    type_: SearchSuggestionType,
) -> Optional[list[str]]:
    """This endpoint requires the `asset.read` permission.

    Args:
        country (Union[Unset, str]):
        include_null (Union[Unset, bool]):
        make (Union[Unset, str]):
        model (Union[Unset, str]):
        state (Union[Unset, str]):
        type_ (SearchSuggestionType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[str]
    """

    return (
        await asyncio_detailed(
            client=client,
            country=country,
            include_null=include_null,
            make=make,
            model=model,
            state=state,
            type_=type_,
        )
    ).parsed
