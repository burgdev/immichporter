import datetime
from collections.abc import Mapping
from io import BytesIO
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="AssetMediaReplaceDto")


@_attrs_define
class AssetMediaReplaceDto:
    """
    Attributes:
        asset_data (File):
        device_asset_id (str):
        device_id (str):
        file_created_at (datetime.datetime):
        file_modified_at (datetime.datetime):
        duration (Union[Unset, str]):
        filename (Union[Unset, str]):
    """

    asset_data: File
    device_asset_id: str
    device_id: str
    file_created_at: datetime.datetime
    file_modified_at: datetime.datetime
    duration: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_data = self.asset_data.to_tuple()

        device_asset_id = self.device_asset_id

        device_id = self.device_id

        file_created_at = self.file_created_at.isoformat()

        file_modified_at = self.file_modified_at.isoformat()

        duration = self.duration

        filename = self.filename

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assetData": asset_data,
                "deviceAssetId": device_asset_id,
                "deviceId": device_id,
                "fileCreatedAt": file_created_at,
                "fileModifiedAt": file_modified_at,
            }
        )
        if duration is not UNSET:
            field_dict["duration"] = duration
        if filename is not UNSET:
            field_dict["filename"] = filename

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

        if not isinstance(self.duration, Unset):
            files.append(
                ("duration", (None, str(self.duration).encode(), "text/plain"))
            )

        if not isinstance(self.filename, Unset):
            files.append(
                ("filename", (None, str(self.filename).encode(), "text/plain"))
            )

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_data = File(payload=BytesIO(d.pop("assetData")))

        device_asset_id = d.pop("deviceAssetId")

        device_id = d.pop("deviceId")

        file_created_at = isoparse(d.pop("fileCreatedAt"))

        file_modified_at = isoparse(d.pop("fileModifiedAt"))

        duration = d.pop("duration", UNSET)

        filename = d.pop("filename", UNSET)

        asset_media_replace_dto = cls(
            asset_data=asset_data,
            device_asset_id=device_asset_id,
            device_id=device_id,
            file_created_at=file_created_at,
            file_modified_at=file_modified_at,
            duration=duration,
            filename=filename,
        )

        asset_media_replace_dto.additional_properties = d
        return asset_media_replace_dto

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
