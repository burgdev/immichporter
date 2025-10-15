from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CheckExistingAssetsDto")


@_attrs_define
class CheckExistingAssetsDto:
    """
    Attributes:
        device_asset_ids (list[str]):
        device_id (str):
    """

    device_asset_ids: list[str]
    device_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        device_asset_ids = self.device_asset_ids

        device_id = self.device_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deviceAssetIds": device_asset_ids,
                "deviceId": device_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        device_asset_ids = cast(list[str], d.pop("deviceAssetIds"))

        device_id = d.pop("deviceId")

        check_existing_assets_dto = cls(
            device_asset_ids=device_asset_ids,
            device_id=device_id,
        )

        check_existing_assets_dto.additional_properties = d
        return check_existing_assets_dto

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
