from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_order import AssetOrder
from ..types import UNSET, Unset

T = TypeVar("T", bound="AlbumsUpdate")


@_attrs_define
class AlbumsUpdate:
    """
    Attributes:
        default_asset_order (Union[Unset, AssetOrder]):
    """

    default_asset_order: Union[Unset, AssetOrder] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_asset_order: Union[Unset, str] = UNSET
        if not isinstance(self.default_asset_order, Unset):
            default_asset_order = self.default_asset_order.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_asset_order is not UNSET:
            field_dict["defaultAssetOrder"] = default_asset_order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _default_asset_order = d.pop("defaultAssetOrder", UNSET)
        default_asset_order: Union[Unset, AssetOrder]
        if isinstance(_default_asset_order, Unset):
            default_asset_order = UNSET
        else:
            default_asset_order = AssetOrder(_default_asset_order)

        albums_update = cls(
            default_asset_order=default_asset_order,
        )

        albums_update.additional_properties = d
        return albums_update

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
