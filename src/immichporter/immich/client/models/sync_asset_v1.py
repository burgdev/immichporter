import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.asset_type_enum import AssetTypeEnum
from ..models.asset_visibility import AssetVisibility

T = TypeVar("T", bound="SyncAssetV1")


@_attrs_define
class SyncAssetV1:
    """
    Attributes:
        checksum (str):
        deleted_at (Union[None, datetime.datetime]):
        duration (Union[None, str]):
        file_created_at (Union[None, datetime.datetime]):
        file_modified_at (Union[None, datetime.datetime]):
        id (str):
        is_favorite (bool):
        library_id (Union[None, str]):
        live_photo_video_id (Union[None, str]):
        local_date_time (Union[None, datetime.datetime]):
        original_file_name (str):
        owner_id (str):
        stack_id (Union[None, str]):
        thumbhash (Union[None, str]):
        type_ (AssetTypeEnum):
        visibility (AssetVisibility):
    """

    checksum: str
    deleted_at: Union[None, datetime.datetime]
    duration: Union[None, str]
    file_created_at: Union[None, datetime.datetime]
    file_modified_at: Union[None, datetime.datetime]
    id: str
    is_favorite: bool
    library_id: Union[None, str]
    live_photo_video_id: Union[None, str]
    local_date_time: Union[None, datetime.datetime]
    original_file_name: str
    owner_id: str
    stack_id: Union[None, str]
    thumbhash: Union[None, str]
    type_: AssetTypeEnum
    visibility: AssetVisibility
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checksum = self.checksum

        deleted_at: Union[None, str]
        if isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        duration: Union[None, str]
        duration = self.duration

        file_created_at: Union[None, str]
        if isinstance(self.file_created_at, datetime.datetime):
            file_created_at = self.file_created_at.isoformat()
        else:
            file_created_at = self.file_created_at

        file_modified_at: Union[None, str]
        if isinstance(self.file_modified_at, datetime.datetime):
            file_modified_at = self.file_modified_at.isoformat()
        else:
            file_modified_at = self.file_modified_at

        id = self.id

        is_favorite = self.is_favorite

        library_id: Union[None, str]
        library_id = self.library_id

        live_photo_video_id: Union[None, str]
        live_photo_video_id = self.live_photo_video_id

        local_date_time: Union[None, str]
        if isinstance(self.local_date_time, datetime.datetime):
            local_date_time = self.local_date_time.isoformat()
        else:
            local_date_time = self.local_date_time

        original_file_name = self.original_file_name

        owner_id = self.owner_id

        stack_id: Union[None, str]
        stack_id = self.stack_id

        thumbhash: Union[None, str]
        thumbhash = self.thumbhash

        type_ = self.type_.value

        visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checksum": checksum,
                "deletedAt": deleted_at,
                "duration": duration,
                "fileCreatedAt": file_created_at,
                "fileModifiedAt": file_modified_at,
                "id": id,
                "isFavorite": is_favorite,
                "libraryId": library_id,
                "livePhotoVideoId": live_photo_video_id,
                "localDateTime": local_date_time,
                "originalFileName": original_file_name,
                "ownerId": owner_id,
                "stackId": stack_id,
                "thumbhash": thumbhash,
                "type": type_,
                "visibility": visibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checksum = d.pop("checksum")

        def _parse_deleted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deleted_at = _parse_deleted_at(d.pop("deletedAt"))

        def _parse_duration(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        duration = _parse_duration(d.pop("duration"))

        def _parse_file_created_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                file_created_at_type_0 = isoparse(data)

                return file_created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        file_created_at = _parse_file_created_at(d.pop("fileCreatedAt"))

        def _parse_file_modified_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                file_modified_at_type_0 = isoparse(data)

                return file_modified_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        file_modified_at = _parse_file_modified_at(d.pop("fileModifiedAt"))

        id = d.pop("id")

        is_favorite = d.pop("isFavorite")

        def _parse_library_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        library_id = _parse_library_id(d.pop("libraryId"))

        def _parse_live_photo_video_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        live_photo_video_id = _parse_live_photo_video_id(d.pop("livePhotoVideoId"))

        def _parse_local_date_time(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                local_date_time_type_0 = isoparse(data)

                return local_date_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        local_date_time = _parse_local_date_time(d.pop("localDateTime"))

        original_file_name = d.pop("originalFileName")

        owner_id = d.pop("ownerId")

        def _parse_stack_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        stack_id = _parse_stack_id(d.pop("stackId"))

        def _parse_thumbhash(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        thumbhash = _parse_thumbhash(d.pop("thumbhash"))

        type_ = AssetTypeEnum(d.pop("type"))

        visibility = AssetVisibility(d.pop("visibility"))

        sync_asset_v1 = cls(
            checksum=checksum,
            deleted_at=deleted_at,
            duration=duration,
            file_created_at=file_created_at,
            file_modified_at=file_modified_at,
            id=id,
            is_favorite=is_favorite,
            library_id=library_id,
            live_photo_video_id=live_photo_video_id,
            local_date_time=local_date_time,
            original_file_name=original_file_name,
            owner_id=owner_id,
            stack_id=stack_id,
            thumbhash=thumbhash,
            type_=type_,
            visibility=visibility,
        )

        sync_asset_v1.additional_properties = d
        return sync_asset_v1

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
