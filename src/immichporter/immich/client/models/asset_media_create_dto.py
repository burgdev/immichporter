from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..models.asset_visibility import AssetVisibility
from ..types import File, FileTypes
from dateutil.parser import isoparse
from io import BytesIO
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
    from ..models.asset_metadata_upsert_item_dto import AssetMetadataUpsertItemDto


T = TypeVar("T", bound="AssetMediaCreateDto")


@_attrs_define
class AssetMediaCreateDto:
    """
    Attributes:
        asset_data (File):
        device_asset_id (str):
        device_id (str):
        file_created_at (datetime.datetime):
        file_modified_at (datetime.datetime):
        metadata (list['AssetMetadataUpsertItemDto']):
        duration (Union[Unset, str]):
        filename (Union[Unset, str]):
        is_favorite (Union[Unset, bool]):
        live_photo_video_id (Union[Unset, UUID]):
        sidecar_data (Union[Unset, File]):
        visibility (Union[Unset, AssetVisibility]):
    """

    asset_data: File
    device_asset_id: str
    device_id: str
    file_created_at: datetime.datetime
    file_modified_at: datetime.datetime
    metadata: list["AssetMetadataUpsertItemDto"]
    duration: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    is_favorite: Union[Unset, bool] = UNSET
    live_photo_video_id: Union[Unset, UUID] = UNSET
    sidecar_data: Union[Unset, File] = UNSET
    visibility: Union[Unset, AssetVisibility] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_data = self.asset_data.to_tuple()

        device_asset_id = self.device_asset_id

        device_id = self.device_id

        file_created_at = self.file_created_at.isoformat()

        file_modified_at = self.file_modified_at.isoformat()

        metadata = []
        for metadata_item_data in self.metadata:
            metadata_item = metadata_item_data.to_dict()
            metadata.append(metadata_item)

        duration = self.duration

        filename = self.filename

        is_favorite = self.is_favorite

        live_photo_video_id: Union[Unset, str] = UNSET
        if not isinstance(self.live_photo_video_id, Unset):
            live_photo_video_id = str(self.live_photo_video_id)

        sidecar_data: Union[Unset, FileTypes] = UNSET
        if not isinstance(self.sidecar_data, Unset):
            sidecar_data = self.sidecar_data.to_tuple()

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assetData": asset_data,
                "deviceAssetId": device_asset_id,
                "deviceId": device_id,
                "fileCreatedAt": file_created_at,
                "fileModifiedAt": file_modified_at,
                "metadata": metadata,
            }
        )
        if duration is not UNSET:
            field_dict["duration"] = duration
        if filename is not UNSET:
            field_dict["filename"] = filename
        if is_favorite is not UNSET:
            field_dict["isFavorite"] = is_favorite
        if live_photo_video_id is not UNSET:
            field_dict["livePhotoVideoId"] = live_photo_video_id
        if sidecar_data is not UNSET:
            field_dict["sidecarData"] = sidecar_data
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("assetData", self.asset_data.to_tuple()))

        files.append(
            ("deviceAssetId", (None, str(self.device_asset_id).encode(), "text/plain"))
        )

        files.append(("deviceId", (None, str(self.device_id).encode(), "text/plain")))

        files.append(
            (
                "fileCreatedAt",
                (None, self.file_created_at.isoformat().encode(), "text/plain"),
            )
        )

        files.append(
            (
                "fileModifiedAt",
                (None, self.file_modified_at.isoformat().encode(), "text/plain"),
            )
        )

        for metadata_item_element in self.metadata:
            files.append(
                (
                    "metadata",
                    (
                        None,
                        json.dumps(metadata_item_element.to_dict()).encode(),
                        "application/json",
                    ),
                )
            )

        if not isinstance(self.duration, Unset):
            files.append(
                ("duration", (None, str(self.duration).encode(), "text/plain"))
            )

        if not isinstance(self.filename, Unset):
            files.append(
                ("filename", (None, str(self.filename).encode(), "text/plain"))
            )

        if not isinstance(self.is_favorite, Unset):
            files.append(
                ("isFavorite", (None, str(self.is_favorite).encode(), "text/plain"))
            )

        if not isinstance(self.live_photo_video_id, Unset):
            files.append(
                (
                    "livePhotoVideoId",
                    (None, str(self.live_photo_video_id), "text/plain"),
                )
            )

        if not isinstance(self.sidecar_data, Unset):
            files.append(("sidecarData", self.sidecar_data.to_tuple()))

        if not isinstance(self.visibility, Unset):
            files.append(
                (
                    "visibility",
                    (None, str(self.visibility.value).encode(), "text/plain"),
                )
            )

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_metadata_upsert_item_dto import AssetMetadataUpsertItemDto

        d = dict(src_dict)
        asset_data = File(payload=BytesIO(d.pop("assetData")))

        device_asset_id = d.pop("deviceAssetId")

        device_id = d.pop("deviceId")

        file_created_at = isoparse(d.pop("fileCreatedAt"))

        file_modified_at = isoparse(d.pop("fileModifiedAt"))

        metadata = []
        _metadata = d.pop("metadata")
        for metadata_item_data in _metadata:
            metadata_item = AssetMetadataUpsertItemDto.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        duration = d.pop("duration", UNSET)

        filename = d.pop("filename", UNSET)

        is_favorite = d.pop("isFavorite", UNSET)

        _live_photo_video_id = d.pop("livePhotoVideoId", UNSET)
        live_photo_video_id: Union[Unset, UUID]
        if isinstance(_live_photo_video_id, Unset):
            live_photo_video_id = UNSET
        else:
            live_photo_video_id = UUID(_live_photo_video_id)

        _sidecar_data = d.pop("sidecarData", UNSET)
        sidecar_data: Union[Unset, File]
        if isinstance(_sidecar_data, Unset):
            sidecar_data = UNSET
        else:
            sidecar_data = File(payload=BytesIO(_sidecar_data))

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, AssetVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = AssetVisibility(_visibility)

        asset_media_create_dto = cls(
            asset_data=asset_data,
            device_asset_id=device_asset_id,
            device_id=device_id,
            file_created_at=file_created_at,
            file_modified_at=file_modified_at,
            metadata=metadata,
            duration=duration,
            filename=filename,
            is_favorite=is_favorite,
            live_photo_video_id=live_photo_video_id,
            sidecar_data=sidecar_data,
            visibility=visibility,
        )

        asset_media_create_dto.additional_properties = d
        return asset_media_create_dto

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
