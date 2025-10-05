import datetime
from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_response_dto import AssetResponseDto
from ...models.asset_type_enum import AssetTypeEnum
from ...models.asset_visibility import AssetVisibility
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    album_ids: Union[Unset, list[UUID]] = UNSET,
    city: Union[None, Unset, str] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    is_encoded: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_motion: Union[Unset, bool] = UNSET,
    is_not_in_album: Union[Unset, bool] = UNSET,
    is_offline: Union[Unset, bool] = UNSET,
    lens_model: Union[None, Unset, str] = UNSET,
    library_id: Union[None, UUID, Unset] = UNSET,
    make: Union[Unset, str] = UNSET,
    min_file_size: Union[Unset, int] = UNSET,
    model: Union[None, Unset, str] = UNSET,
    person_ids: Union[Unset, list[UUID]] = UNSET,
    rating: Union[Unset, float] = UNSET,
    size: Union[Unset, float] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    tag_ids: Union[None, Unset, list[UUID]] = UNSET,
    taken_after: Union[Unset, datetime.datetime] = UNSET,
    taken_before: Union[Unset, datetime.datetime] = UNSET,
    trashed_after: Union[Unset, datetime.datetime] = UNSET,
    trashed_before: Union[Unset, datetime.datetime] = UNSET,
    type_: Union[Unset, AssetTypeEnum] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_deleted: Union[Unset, bool] = UNSET,
    with_exif: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_album_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(album_ids, Unset):
        json_album_ids = []
        for album_ids_item_data in album_ids:
            album_ids_item = str(album_ids_item_data)
            json_album_ids.append(album_ids_item)

    params["albumIds"] = json_album_ids

    json_city: Union[None, Unset, str]
    if isinstance(city, Unset):
        json_city = UNSET
    else:
        json_city = city
    params["city"] = json_city

    json_country: Union[None, Unset, str]
    if isinstance(country, Unset):
        json_country = UNSET
    else:
        json_country = country
    params["country"] = json_country

    json_created_after: Union[Unset, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["createdAfter"] = json_created_after

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["createdBefore"] = json_created_before

    params["deviceId"] = device_id

    params["isEncoded"] = is_encoded

    params["isFavorite"] = is_favorite

    params["isMotion"] = is_motion

    params["isNotInAlbum"] = is_not_in_album

    params["isOffline"] = is_offline

    json_lens_model: Union[None, Unset, str]
    if isinstance(lens_model, Unset):
        json_lens_model = UNSET
    else:
        json_lens_model = lens_model
    params["lensModel"] = json_lens_model

    json_library_id: Union[None, Unset, str]
    if isinstance(library_id, Unset):
        json_library_id = UNSET
    elif isinstance(library_id, UUID):
        json_library_id = str(library_id)
    else:
        json_library_id = library_id
    params["libraryId"] = json_library_id

    params["make"] = make

    params["minFileSize"] = min_file_size

    json_model: Union[None, Unset, str]
    if isinstance(model, Unset):
        json_model = UNSET
    else:
        json_model = model
    params["model"] = json_model

    json_person_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(person_ids, Unset):
        json_person_ids = []
        for person_ids_item_data in person_ids:
            person_ids_item = str(person_ids_item_data)
            json_person_ids.append(person_ids_item)

    params["personIds"] = json_person_ids

    params["rating"] = rating

    params["size"] = size

    json_state: Union[None, Unset, str]
    if isinstance(state, Unset):
        json_state = UNSET
    else:
        json_state = state
    params["state"] = json_state

    json_tag_ids: Union[None, Unset, list[str]]
    if isinstance(tag_ids, Unset):
        json_tag_ids = UNSET
    elif isinstance(tag_ids, list):
        json_tag_ids = []
        for tag_ids_type_0_item_data in tag_ids:
            tag_ids_type_0_item = str(tag_ids_type_0_item_data)
            json_tag_ids.append(tag_ids_type_0_item)

    else:
        json_tag_ids = tag_ids
    params["tagIds"] = json_tag_ids

    json_taken_after: Union[Unset, str] = UNSET
    if not isinstance(taken_after, Unset):
        json_taken_after = taken_after.isoformat()
    params["takenAfter"] = json_taken_after

    json_taken_before: Union[Unset, str] = UNSET
    if not isinstance(taken_before, Unset):
        json_taken_before = taken_before.isoformat()
    params["takenBefore"] = json_taken_before

    json_trashed_after: Union[Unset, str] = UNSET
    if not isinstance(trashed_after, Unset):
        json_trashed_after = trashed_after.isoformat()
    params["trashedAfter"] = json_trashed_after

    json_trashed_before: Union[Unset, str] = UNSET
    if not isinstance(trashed_before, Unset):
        json_trashed_before = trashed_before.isoformat()
    params["trashedBefore"] = json_trashed_before

    json_type_: Union[Unset, str] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    json_updated_after: Union[Unset, str] = UNSET
    if not isinstance(updated_after, Unset):
        json_updated_after = updated_after.isoformat()
    params["updatedAfter"] = json_updated_after

    json_updated_before: Union[Unset, str] = UNSET
    if not isinstance(updated_before, Unset):
        json_updated_before = updated_before.isoformat()
    params["updatedBefore"] = json_updated_before

    json_visibility: Union[Unset, str] = UNSET
    if not isinstance(visibility, Unset):
        json_visibility = visibility.value

    params["visibility"] = json_visibility

    params["withDeleted"] = with_deleted

    params["withExif"] = with_exif

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/search/large-assets",
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
    album_ids: Union[Unset, list[UUID]] = UNSET,
    city: Union[None, Unset, str] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    is_encoded: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_motion: Union[Unset, bool] = UNSET,
    is_not_in_album: Union[Unset, bool] = UNSET,
    is_offline: Union[Unset, bool] = UNSET,
    lens_model: Union[None, Unset, str] = UNSET,
    library_id: Union[None, UUID, Unset] = UNSET,
    make: Union[Unset, str] = UNSET,
    min_file_size: Union[Unset, int] = UNSET,
    model: Union[None, Unset, str] = UNSET,
    person_ids: Union[Unset, list[UUID]] = UNSET,
    rating: Union[Unset, float] = UNSET,
    size: Union[Unset, float] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    tag_ids: Union[None, Unset, list[UUID]] = UNSET,
    taken_after: Union[Unset, datetime.datetime] = UNSET,
    taken_before: Union[Unset, datetime.datetime] = UNSET,
    trashed_after: Union[Unset, datetime.datetime] = UNSET,
    trashed_before: Union[Unset, datetime.datetime] = UNSET,
    type_: Union[Unset, AssetTypeEnum] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_deleted: Union[Unset, bool] = UNSET,
    with_exif: Union[Unset, bool] = UNSET,
) -> Response[list["AssetResponseDto"]]:
    """This endpoint requires the `asset.read` permission.

    Args:
        album_ids (Union[Unset, list[UUID]]):
        city (Union[None, Unset, str]):
        country (Union[None, Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        device_id (Union[Unset, str]):
        is_encoded (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        is_motion (Union[Unset, bool]):
        is_not_in_album (Union[Unset, bool]):
        is_offline (Union[Unset, bool]):
        lens_model (Union[None, Unset, str]):
        library_id (Union[None, UUID, Unset]):
        make (Union[Unset, str]):
        min_file_size (Union[Unset, int]):
        model (Union[None, Unset, str]):
        person_ids (Union[Unset, list[UUID]]):
        rating (Union[Unset, float]):
        size (Union[Unset, float]):
        state (Union[None, Unset, str]):
        tag_ids (Union[None, Unset, list[UUID]]):
        taken_after (Union[Unset, datetime.datetime]):
        taken_before (Union[Unset, datetime.datetime]):
        trashed_after (Union[Unset, datetime.datetime]):
        trashed_before (Union[Unset, datetime.datetime]):
        type_ (Union[Unset, AssetTypeEnum]):
        updated_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        visibility (Union[Unset, AssetVisibility]):
        with_deleted (Union[Unset, bool]):
        with_exif (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AssetResponseDto']]
    """

    kwargs = _get_kwargs(
        album_ids=album_ids,
        city=city,
        country=country,
        created_after=created_after,
        created_before=created_before,
        device_id=device_id,
        is_encoded=is_encoded,
        is_favorite=is_favorite,
        is_motion=is_motion,
        is_not_in_album=is_not_in_album,
        is_offline=is_offline,
        lens_model=lens_model,
        library_id=library_id,
        make=make,
        min_file_size=min_file_size,
        model=model,
        person_ids=person_ids,
        rating=rating,
        size=size,
        state=state,
        tag_ids=tag_ids,
        taken_after=taken_after,
        taken_before=taken_before,
        trashed_after=trashed_after,
        trashed_before=trashed_before,
        type_=type_,
        updated_after=updated_after,
        updated_before=updated_before,
        visibility=visibility,
        with_deleted=with_deleted,
        with_exif=with_exif,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    album_ids: Union[Unset, list[UUID]] = UNSET,
    city: Union[None, Unset, str] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    is_encoded: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_motion: Union[Unset, bool] = UNSET,
    is_not_in_album: Union[Unset, bool] = UNSET,
    is_offline: Union[Unset, bool] = UNSET,
    lens_model: Union[None, Unset, str] = UNSET,
    library_id: Union[None, UUID, Unset] = UNSET,
    make: Union[Unset, str] = UNSET,
    min_file_size: Union[Unset, int] = UNSET,
    model: Union[None, Unset, str] = UNSET,
    person_ids: Union[Unset, list[UUID]] = UNSET,
    rating: Union[Unset, float] = UNSET,
    size: Union[Unset, float] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    tag_ids: Union[None, Unset, list[UUID]] = UNSET,
    taken_after: Union[Unset, datetime.datetime] = UNSET,
    taken_before: Union[Unset, datetime.datetime] = UNSET,
    trashed_after: Union[Unset, datetime.datetime] = UNSET,
    trashed_before: Union[Unset, datetime.datetime] = UNSET,
    type_: Union[Unset, AssetTypeEnum] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_deleted: Union[Unset, bool] = UNSET,
    with_exif: Union[Unset, bool] = UNSET,
) -> Optional[list["AssetResponseDto"]]:
    """This endpoint requires the `asset.read` permission.

    Args:
        album_ids (Union[Unset, list[UUID]]):
        city (Union[None, Unset, str]):
        country (Union[None, Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        device_id (Union[Unset, str]):
        is_encoded (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        is_motion (Union[Unset, bool]):
        is_not_in_album (Union[Unset, bool]):
        is_offline (Union[Unset, bool]):
        lens_model (Union[None, Unset, str]):
        library_id (Union[None, UUID, Unset]):
        make (Union[Unset, str]):
        min_file_size (Union[Unset, int]):
        model (Union[None, Unset, str]):
        person_ids (Union[Unset, list[UUID]]):
        rating (Union[Unset, float]):
        size (Union[Unset, float]):
        state (Union[None, Unset, str]):
        tag_ids (Union[None, Unset, list[UUID]]):
        taken_after (Union[Unset, datetime.datetime]):
        taken_before (Union[Unset, datetime.datetime]):
        trashed_after (Union[Unset, datetime.datetime]):
        trashed_before (Union[Unset, datetime.datetime]):
        type_ (Union[Unset, AssetTypeEnum]):
        updated_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        visibility (Union[Unset, AssetVisibility]):
        with_deleted (Union[Unset, bool]):
        with_exif (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AssetResponseDto']
    """

    return sync_detailed(
        client=client,
        album_ids=album_ids,
        city=city,
        country=country,
        created_after=created_after,
        created_before=created_before,
        device_id=device_id,
        is_encoded=is_encoded,
        is_favorite=is_favorite,
        is_motion=is_motion,
        is_not_in_album=is_not_in_album,
        is_offline=is_offline,
        lens_model=lens_model,
        library_id=library_id,
        make=make,
        min_file_size=min_file_size,
        model=model,
        person_ids=person_ids,
        rating=rating,
        size=size,
        state=state,
        tag_ids=tag_ids,
        taken_after=taken_after,
        taken_before=taken_before,
        trashed_after=trashed_after,
        trashed_before=trashed_before,
        type_=type_,
        updated_after=updated_after,
        updated_before=updated_before,
        visibility=visibility,
        with_deleted=with_deleted,
        with_exif=with_exif,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    album_ids: Union[Unset, list[UUID]] = UNSET,
    city: Union[None, Unset, str] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    is_encoded: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_motion: Union[Unset, bool] = UNSET,
    is_not_in_album: Union[Unset, bool] = UNSET,
    is_offline: Union[Unset, bool] = UNSET,
    lens_model: Union[None, Unset, str] = UNSET,
    library_id: Union[None, UUID, Unset] = UNSET,
    make: Union[Unset, str] = UNSET,
    min_file_size: Union[Unset, int] = UNSET,
    model: Union[None, Unset, str] = UNSET,
    person_ids: Union[Unset, list[UUID]] = UNSET,
    rating: Union[Unset, float] = UNSET,
    size: Union[Unset, float] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    tag_ids: Union[None, Unset, list[UUID]] = UNSET,
    taken_after: Union[Unset, datetime.datetime] = UNSET,
    taken_before: Union[Unset, datetime.datetime] = UNSET,
    trashed_after: Union[Unset, datetime.datetime] = UNSET,
    trashed_before: Union[Unset, datetime.datetime] = UNSET,
    type_: Union[Unset, AssetTypeEnum] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_deleted: Union[Unset, bool] = UNSET,
    with_exif: Union[Unset, bool] = UNSET,
) -> Response[list["AssetResponseDto"]]:
    """This endpoint requires the `asset.read` permission.

    Args:
        album_ids (Union[Unset, list[UUID]]):
        city (Union[None, Unset, str]):
        country (Union[None, Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        device_id (Union[Unset, str]):
        is_encoded (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        is_motion (Union[Unset, bool]):
        is_not_in_album (Union[Unset, bool]):
        is_offline (Union[Unset, bool]):
        lens_model (Union[None, Unset, str]):
        library_id (Union[None, UUID, Unset]):
        make (Union[Unset, str]):
        min_file_size (Union[Unset, int]):
        model (Union[None, Unset, str]):
        person_ids (Union[Unset, list[UUID]]):
        rating (Union[Unset, float]):
        size (Union[Unset, float]):
        state (Union[None, Unset, str]):
        tag_ids (Union[None, Unset, list[UUID]]):
        taken_after (Union[Unset, datetime.datetime]):
        taken_before (Union[Unset, datetime.datetime]):
        trashed_after (Union[Unset, datetime.datetime]):
        trashed_before (Union[Unset, datetime.datetime]):
        type_ (Union[Unset, AssetTypeEnum]):
        updated_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        visibility (Union[Unset, AssetVisibility]):
        with_deleted (Union[Unset, bool]):
        with_exif (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AssetResponseDto']]
    """

    kwargs = _get_kwargs(
        album_ids=album_ids,
        city=city,
        country=country,
        created_after=created_after,
        created_before=created_before,
        device_id=device_id,
        is_encoded=is_encoded,
        is_favorite=is_favorite,
        is_motion=is_motion,
        is_not_in_album=is_not_in_album,
        is_offline=is_offline,
        lens_model=lens_model,
        library_id=library_id,
        make=make,
        min_file_size=min_file_size,
        model=model,
        person_ids=person_ids,
        rating=rating,
        size=size,
        state=state,
        tag_ids=tag_ids,
        taken_after=taken_after,
        taken_before=taken_before,
        trashed_after=trashed_after,
        trashed_before=trashed_before,
        type_=type_,
        updated_after=updated_after,
        updated_before=updated_before,
        visibility=visibility,
        with_deleted=with_deleted,
        with_exif=with_exif,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    album_ids: Union[Unset, list[UUID]] = UNSET,
    city: Union[None, Unset, str] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    is_encoded: Union[Unset, bool] = UNSET,
    is_favorite: Union[Unset, bool] = UNSET,
    is_motion: Union[Unset, bool] = UNSET,
    is_not_in_album: Union[Unset, bool] = UNSET,
    is_offline: Union[Unset, bool] = UNSET,
    lens_model: Union[None, Unset, str] = UNSET,
    library_id: Union[None, UUID, Unset] = UNSET,
    make: Union[Unset, str] = UNSET,
    min_file_size: Union[Unset, int] = UNSET,
    model: Union[None, Unset, str] = UNSET,
    person_ids: Union[Unset, list[UUID]] = UNSET,
    rating: Union[Unset, float] = UNSET,
    size: Union[Unset, float] = UNSET,
    state: Union[None, Unset, str] = UNSET,
    tag_ids: Union[None, Unset, list[UUID]] = UNSET,
    taken_after: Union[Unset, datetime.datetime] = UNSET,
    taken_before: Union[Unset, datetime.datetime] = UNSET,
    trashed_after: Union[Unset, datetime.datetime] = UNSET,
    trashed_before: Union[Unset, datetime.datetime] = UNSET,
    type_: Union[Unset, AssetTypeEnum] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    visibility: Union[Unset, AssetVisibility] = UNSET,
    with_deleted: Union[Unset, bool] = UNSET,
    with_exif: Union[Unset, bool] = UNSET,
) -> Optional[list["AssetResponseDto"]]:
    """This endpoint requires the `asset.read` permission.

    Args:
        album_ids (Union[Unset, list[UUID]]):
        city (Union[None, Unset, str]):
        country (Union[None, Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        device_id (Union[Unset, str]):
        is_encoded (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        is_motion (Union[Unset, bool]):
        is_not_in_album (Union[Unset, bool]):
        is_offline (Union[Unset, bool]):
        lens_model (Union[None, Unset, str]):
        library_id (Union[None, UUID, Unset]):
        make (Union[Unset, str]):
        min_file_size (Union[Unset, int]):
        model (Union[None, Unset, str]):
        person_ids (Union[Unset, list[UUID]]):
        rating (Union[Unset, float]):
        size (Union[Unset, float]):
        state (Union[None, Unset, str]):
        tag_ids (Union[None, Unset, list[UUID]]):
        taken_after (Union[Unset, datetime.datetime]):
        taken_before (Union[Unset, datetime.datetime]):
        trashed_after (Union[Unset, datetime.datetime]):
        trashed_before (Union[Unset, datetime.datetime]):
        type_ (Union[Unset, AssetTypeEnum]):
        updated_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        visibility (Union[Unset, AssetVisibility]):
        with_deleted (Union[Unset, bool]):
        with_exif (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AssetResponseDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            album_ids=album_ids,
            city=city,
            country=country,
            created_after=created_after,
            created_before=created_before,
            device_id=device_id,
            is_encoded=is_encoded,
            is_favorite=is_favorite,
            is_motion=is_motion,
            is_not_in_album=is_not_in_album,
            is_offline=is_offline,
            lens_model=lens_model,
            library_id=library_id,
            make=make,
            min_file_size=min_file_size,
            model=model,
            person_ids=person_ids,
            rating=rating,
            size=size,
            state=state,
            tag_ids=tag_ids,
            taken_after=taken_after,
            taken_before=taken_before,
            trashed_after=trashed_after,
            trashed_before=trashed_before,
            type_=type_,
            updated_after=updated_after,
            updated_before=updated_before,
            visibility=visibility,
            with_deleted=with_deleted,
            with_exif=with_exif,
        )
    ).parsed
