from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AssetStackResponseDto")


@_attrs_define
class AssetStackResponseDto:
    """
    Attributes:
        asset_count (int):
        id (str):
        primary_asset_id (str):
    """

    asset_count: int
    id: str
    primary_asset_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_count = self.asset_count

        id = self.id

        primary_asset_id = self.primary_asset_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assetCount": asset_count,
                "id": id,
                "primaryAssetId": primary_asset_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_count = d.pop("assetCount")

        id = d.pop("id")

        primary_asset_id = d.pop("primaryAssetId")

        asset_stack_response_dto = cls(
            asset_count=asset_count,
            id=id,
            primary_asset_id=primary_asset_id,
        )

        asset_stack_response_dto.additional_properties = d
        return asset_stack_response_dto

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
