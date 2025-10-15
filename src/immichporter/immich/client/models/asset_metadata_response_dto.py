import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.asset_metadata_key import AssetMetadataKey

if TYPE_CHECKING:
    from ..models.asset_metadata_response_dto_value import AssetMetadataResponseDtoValue


T = TypeVar("T", bound="AssetMetadataResponseDto")


@_attrs_define
class AssetMetadataResponseDto:
    """
    Attributes:
        key (AssetMetadataKey):
        updated_at (datetime.datetime):
        value (AssetMetadataResponseDtoValue):
    """

    key: AssetMetadataKey
    updated_at: datetime.datetime
    value: "AssetMetadataResponseDtoValue"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key.value

        updated_at = self.updated_at.isoformat()

        value = self.value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "updatedAt": updated_at,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_metadata_response_dto_value import (
            AssetMetadataResponseDtoValue,
        )

        d = dict(src_dict)
        key = AssetMetadataKey(d.pop("key"))

        updated_at = isoparse(d.pop("updatedAt"))

        value = AssetMetadataResponseDtoValue.from_dict(d.pop("value"))

        asset_metadata_response_dto = cls(
            key=key,
            updated_at=updated_at,
            value=value,
        )

        asset_metadata_response_dto.additional_properties = d
        return asset_metadata_response_dto

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
