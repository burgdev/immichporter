import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.asset_order import AssetOrder
from ..models.asset_type_enum import AssetTypeEnum
from ..models.asset_visibility import AssetVisibility
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataSearchDto")


@_attrs_define
class MetadataSearchDto:
    """
    Attributes:
        album_ids (Union[Unset, list[UUID]]):
        checksum (Union[Unset, str]):
        city (Union[None, Unset, str]):
        country (Union[None, Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        device_asset_id (Union[Unset, str]):
        device_id (Union[Unset, str]):
        encoded_video_path (Union[Unset, str]):
        id (Union[Unset, UUID]):
        is_encoded (Union[Unset, bool]):
        is_favorite (Union[Unset, bool]):
        is_motion (Union[Unset, bool]):
        is_not_in_album (Union[Unset, bool]):
        is_offline (Union[Unset, bool]):
        lens_model (Union[None, Unset, str]):
        library_id (Union[None, UUID, Unset]):
        make (Union[Unset, str]):
        model (Union[None, Unset, str]):
        order (Union[Unset, AssetOrder]):  Default: AssetOrder.DESC.
        original_file_name (Union[Unset, str]):
        original_path (Union[Unset, str]):
        page (Union[Unset, float]):
        person_ids (Union[Unset, list[UUID]]):
        preview_path (Union[Unset, str]):
        rating (Union[Unset, float]):
        size (Union[Unset, float]):
        state (Union[None, Unset, str]):
        tag_ids (Union[None, Unset, list[UUID]]):
        taken_after (Union[Unset, datetime.datetime]):
        taken_before (Union[Unset, datetime.datetime]):
        thumbnail_path (Union[Unset, str]):
        trashed_after (Union[Unset, datetime.datetime]):
        trashed_before (Union[Unset, datetime.datetime]):
        type_ (Union[Unset, AssetTypeEnum]):
        updated_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        visibility (Union[Unset, AssetVisibility]):
        with_deleted (Union[Unset, bool]):
        with_exif (Union[Unset, bool]):
        with_people (Union[Unset, bool]):
        with_stacked (Union[Unset, bool]):
    """

    album_ids: Union[Unset, list[UUID]] = UNSET
    checksum: Union[Unset, str] = UNSET
    city: Union[None, Unset, str] = UNSET
    country: Union[None, Unset, str] = UNSET
    created_after: Union[Unset, datetime.datetime] = UNSET
    created_before: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    device_asset_id: Union[Unset, str] = UNSET
    device_id: Union[Unset, str] = UNSET
    encoded_video_path: Union[Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    is_encoded: Union[Unset, bool] = UNSET
    is_favorite: Union[Unset, bool] = UNSET
    is_motion: Union[Unset, bool] = UNSET
    is_not_in_album: Union[Unset, bool] = UNSET
    is_offline: Union[Unset, bool] = UNSET
    lens_model: Union[None, Unset, str] = UNSET
    library_id: Union[None, UUID, Unset] = UNSET
    make: Union[Unset, str] = UNSET
    model: Union[None, Unset, str] = UNSET
    order: Union[Unset, AssetOrder] = AssetOrder.DESC
    original_file_name: Union[Unset, str] = UNSET
    original_path: Union[Unset, str] = UNSET
    page: Union[Unset, float] = UNSET
    person_ids: Union[Unset, list[UUID]] = UNSET
    preview_path: Union[Unset, str] = UNSET
    rating: Union[Unset, float] = UNSET
    size: Union[Unset, float] = UNSET
    state: Union[None, Unset, str] = UNSET
    tag_ids: Union[None, Unset, list[UUID]] = UNSET
    taken_after: Union[Unset, datetime.datetime] = UNSET
    taken_before: Union[Unset, datetime.datetime] = UNSET
    thumbnail_path: Union[Unset, str] = UNSET
    trashed_after: Union[Unset, datetime.datetime] = UNSET
    trashed_before: Union[Unset, datetime.datetime] = UNSET
    type_: Union[Unset, AssetTypeEnum] = UNSET
    updated_after: Union[Unset, datetime.datetime] = UNSET
    updated_before: Union[Unset, datetime.datetime] = UNSET
    visibility: Union[Unset, AssetVisibility] = UNSET
    with_deleted: Union[Unset, bool] = UNSET
    with_exif: Union[Unset, bool] = UNSET
    with_people: Union[Unset, bool] = UNSET
    with_stacked: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        album_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.album_ids, Unset):
            album_ids = []
            for album_ids_item_data in self.album_ids:
                album_ids_item = str(album_ids_item_data)
                album_ids.append(album_ids_item)

        checksum = self.checksum

        city: Union[None, Unset, str]
        if isinstance(self.city, Unset):
            city = UNSET
        else:
            city = self.city

        country: Union[None, Unset, str]
        if isinstance(self.country, Unset):
            country = UNSET
        else:
            country = self.country

        created_after: Union[Unset, str] = UNSET
        if not isinstance(self.created_after, Unset):
            created_after = self.created_after.isoformat()

        created_before: Union[Unset, str] = UNSET
        if not isinstance(self.created_before, Unset):
            created_before = self.created_before.isoformat()

        description = self.description

        device_asset_id = self.device_asset_id

        device_id = self.device_id

        encoded_video_path = self.encoded_video_path

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        is_encoded = self.is_encoded

        is_favorite = self.is_favorite

        is_motion = self.is_motion

        is_not_in_album = self.is_not_in_album

        is_offline = self.is_offline

        lens_model: Union[None, Unset, str]
        if isinstance(self.lens_model, Unset):
            lens_model = UNSET
        else:
            lens_model = self.lens_model

        library_id: Union[None, Unset, str]
        if isinstance(self.library_id, Unset):
            library_id = UNSET
        elif isinstance(self.library_id, UUID):
            library_id = str(self.library_id)
        else:
            library_id = self.library_id

        make = self.make

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        order: Union[Unset, str] = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.value

        original_file_name = self.original_file_name

        original_path = self.original_path

        page = self.page

        person_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.person_ids, Unset):
            person_ids = []
            for person_ids_item_data in self.person_ids:
                person_ids_item = str(person_ids_item_data)
                person_ids.append(person_ids_item)

        preview_path = self.preview_path

        rating = self.rating

        size = self.size

        state: Union[None, Unset, str]
        if isinstance(self.state, Unset):
            state = UNSET
        else:
            state = self.state

        tag_ids: Union[None, Unset, list[str]]
        if isinstance(self.tag_ids, Unset):
            tag_ids = UNSET
        elif isinstance(self.tag_ids, list):
            tag_ids = []
            for tag_ids_type_0_item_data in self.tag_ids:
                tag_ids_type_0_item = str(tag_ids_type_0_item_data)
                tag_ids.append(tag_ids_type_0_item)

        else:
            tag_ids = self.tag_ids

        taken_after: Union[Unset, str] = UNSET
        if not isinstance(self.taken_after, Unset):
            taken_after = self.taken_after.isoformat()

        taken_before: Union[Unset, str] = UNSET
        if not isinstance(self.taken_before, Unset):
            taken_before = self.taken_before.isoformat()

        thumbnail_path = self.thumbnail_path

        trashed_after: Union[Unset, str] = UNSET
        if not isinstance(self.trashed_after, Unset):
            trashed_after = self.trashed_after.isoformat()

        trashed_before: Union[Unset, str] = UNSET
        if not isinstance(self.trashed_before, Unset):
            trashed_before = self.trashed_before.isoformat()

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        updated_after: Union[Unset, str] = UNSET
        if not isinstance(self.updated_after, Unset):
            updated_after = self.updated_after.isoformat()

        updated_before: Union[Unset, str] = UNSET
        if not isinstance(self.updated_before, Unset):
            updated_before = self.updated_before.isoformat()

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        with_deleted = self.with_deleted

        with_exif = self.with_exif

        with_people = self.with_people

        with_stacked = self.with_stacked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if album_ids is not UNSET:
            field_dict["albumIds"] = album_ids
        if checksum is not UNSET:
            field_dict["checksum"] = checksum
        if city is not UNSET:
            field_dict["city"] = city
        if country is not UNSET:
            field_dict["country"] = country
        if created_after is not UNSET:
            field_dict["createdAfter"] = created_after
        if created_before is not UNSET:
            field_dict["createdBefore"] = created_before
        if description is not UNSET:
            field_dict["description"] = description
        if device_asset_id is not UNSET:
            field_dict["deviceAssetId"] = device_asset_id
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if encoded_video_path is not UNSET:
            field_dict["encodedVideoPath"] = encoded_video_path
        if id is not UNSET:
            field_dict["id"] = id
        if is_encoded is not UNSET:
            field_dict["isEncoded"] = is_encoded
        if is_favorite is not UNSET:
            field_dict["isFavorite"] = is_favorite
        if is_motion is not UNSET:
            field_dict["isMotion"] = is_motion
        if is_not_in_album is not UNSET:
            field_dict["isNotInAlbum"] = is_not_in_album
        if is_offline is not UNSET:
            field_dict["isOffline"] = is_offline
        if lens_model is not UNSET:
            field_dict["lensModel"] = lens_model
        if library_id is not UNSET:
            field_dict["libraryId"] = library_id
        if make is not UNSET:
            field_dict["make"] = make
        if model is not UNSET:
            field_dict["model"] = model
        if order is not UNSET:
            field_dict["order"] = order
        if original_file_name is not UNSET:
            field_dict["originalFileName"] = original_file_name
        if original_path is not UNSET:
            field_dict["originalPath"] = original_path
        if page is not UNSET:
            field_dict["page"] = page
        if person_ids is not UNSET:
            field_dict["personIds"] = person_ids
        if preview_path is not UNSET:
            field_dict["previewPath"] = preview_path
        if rating is not UNSET:
            field_dict["rating"] = rating
        if size is not UNSET:
            field_dict["size"] = size
        if state is not UNSET:
            field_dict["state"] = state
        if tag_ids is not UNSET:
            field_dict["tagIds"] = tag_ids
        if taken_after is not UNSET:
            field_dict["takenAfter"] = taken_after
        if taken_before is not UNSET:
            field_dict["takenBefore"] = taken_before
        if thumbnail_path is not UNSET:
            field_dict["thumbnailPath"] = thumbnail_path
        if trashed_after is not UNSET:
            field_dict["trashedAfter"] = trashed_after
        if trashed_before is not UNSET:
            field_dict["trashedBefore"] = trashed_before
        if type_ is not UNSET:
            field_dict["type"] = type_
        if updated_after is not UNSET:
            field_dict["updatedAfter"] = updated_after
        if updated_before is not UNSET:
            field_dict["updatedBefore"] = updated_before
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if with_deleted is not UNSET:
            field_dict["withDeleted"] = with_deleted
        if with_exif is not UNSET:
            field_dict["withExif"] = with_exif
        if with_people is not UNSET:
            field_dict["withPeople"] = with_people
        if with_stacked is not UNSET:
            field_dict["withStacked"] = with_stacked

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        album_ids = []
        _album_ids = d.pop("albumIds", UNSET)
        for album_ids_item_data in _album_ids or []:
            album_ids_item = UUID(album_ids_item_data)

            album_ids.append(album_ids_item)

        checksum = d.pop("checksum", UNSET)

        def _parse_city(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        city = _parse_city(d.pop("city", UNSET))

        def _parse_country(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        country = _parse_country(d.pop("country", UNSET))

        _created_after = d.pop("createdAfter", UNSET)
        created_after: Union[Unset, datetime.datetime]
        if isinstance(_created_after, Unset):
            created_after = UNSET
        else:
            created_after = isoparse(_created_after)

        _created_before = d.pop("createdBefore", UNSET)
        created_before: Union[Unset, datetime.datetime]
        if isinstance(_created_before, Unset):
            created_before = UNSET
        else:
            created_before = isoparse(_created_before)

        description = d.pop("description", UNSET)

        device_asset_id = d.pop("deviceAssetId", UNSET)

        device_id = d.pop("deviceId", UNSET)

        encoded_video_path = d.pop("encodedVideoPath", UNSET)

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        is_encoded = d.pop("isEncoded", UNSET)

        is_favorite = d.pop("isFavorite", UNSET)

        is_motion = d.pop("isMotion", UNSET)

        is_not_in_album = d.pop("isNotInAlbum", UNSET)

        is_offline = d.pop("isOffline", UNSET)

        def _parse_lens_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        lens_model = _parse_lens_model(d.pop("lensModel", UNSET))

        def _parse_library_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                library_id_type_0 = UUID(data)

                return library_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        library_id = _parse_library_id(d.pop("libraryId", UNSET))

        make = d.pop("make", UNSET)

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        _order = d.pop("order", UNSET)
        order: Union[Unset, AssetOrder]
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = AssetOrder(_order)

        original_file_name = d.pop("originalFileName", UNSET)

        original_path = d.pop("originalPath", UNSET)

        page = d.pop("page", UNSET)

        person_ids = []
        _person_ids = d.pop("personIds", UNSET)
        for person_ids_item_data in _person_ids or []:
            person_ids_item = UUID(person_ids_item_data)

            person_ids.append(person_ids_item)

        preview_path = d.pop("previewPath", UNSET)

        rating = d.pop("rating", UNSET)

        size = d.pop("size", UNSET)

        def _parse_state(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        state = _parse_state(d.pop("state", UNSET))

        def _parse_tag_ids(data: object) -> Union[None, Unset, list[UUID]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tag_ids_type_0 = []
                _tag_ids_type_0 = data
                for tag_ids_type_0_item_data in _tag_ids_type_0:
                    tag_ids_type_0_item = UUID(tag_ids_type_0_item_data)

                    tag_ids_type_0.append(tag_ids_type_0_item)

                return tag_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[UUID]], data)

        tag_ids = _parse_tag_ids(d.pop("tagIds", UNSET))

        _taken_after = d.pop("takenAfter", UNSET)
        taken_after: Union[Unset, datetime.datetime]
        if isinstance(_taken_after, Unset):
            taken_after = UNSET
        else:
            taken_after = isoparse(_taken_after)

        _taken_before = d.pop("takenBefore", UNSET)
        taken_before: Union[Unset, datetime.datetime]
        if isinstance(_taken_before, Unset):
            taken_before = UNSET
        else:
            taken_before = isoparse(_taken_before)

        thumbnail_path = d.pop("thumbnailPath", UNSET)

        _trashed_after = d.pop("trashedAfter", UNSET)
        trashed_after: Union[Unset, datetime.datetime]
        if isinstance(_trashed_after, Unset):
            trashed_after = UNSET
        else:
            trashed_after = isoparse(_trashed_after)

        _trashed_before = d.pop("trashedBefore", UNSET)
        trashed_before: Union[Unset, datetime.datetime]
        if isinstance(_trashed_before, Unset):
            trashed_before = UNSET
        else:
            trashed_before = isoparse(_trashed_before)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AssetTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = AssetTypeEnum(_type_)

        _updated_after = d.pop("updatedAfter", UNSET)
        updated_after: Union[Unset, datetime.datetime]
        if isinstance(_updated_after, Unset):
            updated_after = UNSET
        else:
            updated_after = isoparse(_updated_after)

        _updated_before = d.pop("updatedBefore", UNSET)
        updated_before: Union[Unset, datetime.datetime]
        if isinstance(_updated_before, Unset):
            updated_before = UNSET
        else:
            updated_before = isoparse(_updated_before)

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, AssetVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = AssetVisibility(_visibility)

        with_deleted = d.pop("withDeleted", UNSET)

        with_exif = d.pop("withExif", UNSET)

        with_people = d.pop("withPeople", UNSET)

        with_stacked = d.pop("withStacked", UNSET)

        metadata_search_dto = cls(
            album_ids=album_ids,
            checksum=checksum,
            city=city,
            country=country,
            created_after=created_after,
            created_before=created_before,
            description=description,
            device_asset_id=device_asset_id,
            device_id=device_id,
            encoded_video_path=encoded_video_path,
            id=id,
            is_encoded=is_encoded,
            is_favorite=is_favorite,
            is_motion=is_motion,
            is_not_in_album=is_not_in_album,
            is_offline=is_offline,
            lens_model=lens_model,
            library_id=library_id,
            make=make,
            model=model,
            order=order,
            original_file_name=original_file_name,
            original_path=original_path,
            page=page,
            person_ids=person_ids,
            preview_path=preview_path,
            rating=rating,
            size=size,
            state=state,
            tag_ids=tag_ids,
            taken_after=taken_after,
            taken_before=taken_before,
            thumbnail_path=thumbnail_path,
            trashed_after=trashed_after,
            trashed_before=trashed_before,
            type_=type_,
            updated_after=updated_after,
            updated_before=updated_before,
            visibility=visibility,
            with_deleted=with_deleted,
            with_exif=with_exif,
            with_people=with_people,
            with_stacked=with_stacked,
        )

        metadata_search_dto.additional_properties = d
        return metadata_search_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
