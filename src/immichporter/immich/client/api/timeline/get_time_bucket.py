from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_order import AssetOrder
from ...models.asset_visibility import AssetVisibility
from ...models.time_bucket_asset_response_dto import TimeBucketAssetResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    album_id: Union[Unset, UUID] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    order: Union[Unset, AssetOrder] = UNSET,
    person_id: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    tag_id: Union[Unset, UUID] = UNSET,
    time_bucket: str,
    user_id: Union[Unset, UUID] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_coordinates: Union[Unset, bool] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_stacked: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_album_id: Union[Unset, str] = UNSET
    if not isinstance(album_id, Unset):
        json_album_id = str(album_id)
    params["albumId"] = json_album_id

    params["isFavorite"] = is_favorite

    params["isTrashed"] = is_trashed

    params["key"] = key

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    json_person_id: Union[Unset, str] = UNSET
    if not isinstance(person_id, Unset):
        json_person_id = str(person_id)
    params["personId"] = json_person_id

    params["slug"] = slug

    json_tag_id: Union[Unset, str] = UNSET
    if not isinstance(tag_id, Unset):
        json_tag_id = str(tag_id)
    params["tagId"] = json_tag_id

    params["timeBucket"] = time_bucket

    json_user_id: Union[Unset, str] = UNSET
    if not isinstance(user_id, Unset):
        json_user_id = str(user_id)
    params["userId"] = json_user_id

    json_visibility: Union[Unset, str] = UNSET
    if not isinstance(visibility, Unset):
        json_visibility = visibility.value

    params["visibility"] = json_visibility

    params["withCoordinates"] = with_coordinates

    params["withPartners"] = with_partners

    params["withStacked"] = with_stacked

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/timeline/bucket",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TimeBucketAssetResponseDto]:
    if response.status_code == 200:
        response_200 = TimeBucketAssetResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TimeBucketAssetResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    album_id: Union[Unset, UUID] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    order: Union[Unset, AssetOrder] = UNSET,
    person_id: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    tag_id: Union[Unset, UUID] = UNSET,
    time_bucket: str,
    user_id: Union[Unset, UUID] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_coordinates: Union[Unset, bool] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_stacked: Union[Unset, bool] = UNSET,
) -> Response[TimeBucketAssetResponseDto]:
    """This endpoint requires the `asset.read` permission.

    Args:
        album_id (Union[Unset, UUID]):
        is_favorite (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        key (Union[Unset, str]):
        order (Union[Unset, AssetOrder]):
        person_id (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        tag_id (Union[Unset, UUID]):
        time_bucket (str):  Example: 2024-01-01.
        user_id (Union[Unset, UUID]):
        visibility (Union[Unset, AssetVisibility]):
        with_coordinates (Union[Unset, bool]):
        with_partners (Union[Unset, bool]):
        with_stacked (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TimeBucketAssetResponseDto]
    """

    kwargs = _get_kwargs(
        album_id=album_id,
        is_favorite=is_favorite,
        is_trashed=is_trashed,
        key=key,
        order=order,
        person_id=person_id,
        slug=slug,
        tag_id=tag_id,
        time_bucket=time_bucket,
        user_id=user_id,
        visibility=visibility,
        with_coordinates=with_coordinates,
        with_partners=with_partners,
        with_stacked=with_stacked,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    album_id: Union[Unset, UUID] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    order: Union[Unset, AssetOrder] = UNSET,
    person_id: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    tag_id: Union[Unset, UUID] = UNSET,
    time_bucket: str,
    user_id: Union[Unset, UUID] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_coordinates: Union[Unset, bool] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_stacked: Union[Unset, bool] = UNSET,
) -> Optional[TimeBucketAssetResponseDto]:
    """This endpoint requires the `asset.read` permission.

    Args:
        album_id (Union[Unset, UUID]):
        is_favorite (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        key (Union[Unset, str]):
        order (Union[Unset, AssetOrder]):
        person_id (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        tag_id (Union[Unset, UUID]):
        time_bucket (str):  Example: 2024-01-01.
        user_id (Union[Unset, UUID]):
        visibility (Union[Unset, AssetVisibility]):
        with_coordinates (Union[Unset, bool]):
        with_partners (Union[Unset, bool]):
        with_stacked (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TimeBucketAssetResponseDto
    """

    return sync_detailed(
        client=client,
        album_id=album_id,
        is_favorite=is_favorite,
        is_trashed=is_trashed,
        key=key,
        order=order,
        person_id=person_id,
        slug=slug,
        tag_id=tag_id,
        time_bucket=time_bucket,
        user_id=user_id,
        visibility=visibility,
        with_coordinates=with_coordinates,
        with_partners=with_partners,
        with_stacked=with_stacked,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    album_id: Union[Unset, UUID] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    order: Union[Unset, AssetOrder] = UNSET,
    person_id: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    tag_id: Union[Unset, UUID] = UNSET,
    time_bucket: str,
    user_id: Union[Unset, UUID] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_coordinates: Union[Unset, bool] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_stacked: Union[Unset, bool] = UNSET,
) -> Response[TimeBucketAssetResponseDto]:
    """This endpoint requires the `asset.read` permission.

    Args:
        album_id (Union[Unset, UUID]):
        is_favorite (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        key (Union[Unset, str]):
        order (Union[Unset, AssetOrder]):
        person_id (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        tag_id (Union[Unset, UUID]):
        time_bucket (str):  Example: 2024-01-01.
        user_id (Union[Unset, UUID]):
        visibility (Union[Unset, AssetVisibility]):
        with_coordinates (Union[Unset, bool]):
        with_partners (Union[Unset, bool]):
        with_stacked (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TimeBucketAssetResponseDto]
    """

    kwargs = _get_kwargs(
        album_id=album_id,
        is_favorite=is_favorite,
        is_trashed=is_trashed,
        key=key,
        order=order,
        person_id=person_id,
        slug=slug,
        tag_id=tag_id,
        time_bucket=time_bucket,
        user_id=user_id,
        visibility=visibility,
        with_coordinates=with_coordinates,
        with_partners=with_partners,
        with_stacked=with_stacked,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    album_id: Union[Unset, UUID] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_trashed: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    order: Union[Unset, AssetOrder] = UNSET,
    person_id: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    tag_id: Union[Unset, UUID] = UNSET,
    time_bucket: str,
    user_id: Union[Unset, UUID] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_coordinates: Union[Unset, bool] = UNSET,
    with_partners: Union[Unset, bool] = UNSET,
    with_stacked: Union[Unset, bool] = UNSET,
) -> Optional[TimeBucketAssetResponseDto]:
    """This endpoint requires the `asset.read` permission.

    Args:
        album_id (Union[Unset, UUID]):
        is_favorite (Union[Unset, bool]):
        is_trashed (Union[Unset, bool]):
        key (Union[Unset, str]):
        order (Union[Unset, AssetOrder]):
        person_id (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        tag_id (Union[Unset, UUID]):
        time_bucket (str):  Example: 2024-01-01.
        user_id (Union[Unset, UUID]):
        visibility (Union[Unset, AssetVisibility]):
        with_coordinates (Union[Unset, bool]):
        with_partners (Union[Unset, bool]):
        with_stacked (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TimeBucketAssetResponseDto
    """

    return (
        await asyncio_detailed(
            client=client,
            album_id=album_id,
            is_favorite=is_favorite,
            is_trashed=is_trashed,
            key=key,
            order=order,
            person_id=person_id,
            slug=slug,
            tag_id=tag_id,
            time_bucket=time_bucket,
            user_id=user_id,
            visibility=visibility,
            with_coordinates=with_coordinates,
            with_partners=with_partners,
            with_stacked=with_stacked,
        )
    ).parsed
