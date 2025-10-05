from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_order import AssetOrder

T = TypeVar("T", bound="AlbumsResponse")


@_attrs_define
class AlbumsResponse:
    """
    Attributes:
        default_asset_order (AssetOrder):  Default: AssetOrder.DESC.
    """

    default_asset_order: AssetOrder = AssetOrder.DESC
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_asset_order = self.default_asset_order.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "defaultAssetOrder": default_asset_order,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default_asset_order = AssetOrder(d.pop("defaultAssetOrder"))

        albums_response = cls(
            default_asset_order=default_asset_order,
        )

        albums_response.additional_properties = d
        return albums_response

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
