from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AlbumsAddAssetsDto")


@_attrs_define
class AlbumsAddAssetsDto:
    """
    Attributes:
        album_ids (list[UUID]):
        asset_ids (list[UUID]):
    """

    album_ids: list[UUID]
    asset_ids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        album_ids = []
        for album_ids_item_data in self.album_ids:
            album_ids_item = str(album_ids_item_data)
            album_ids.append(album_ids_item)

        asset_ids = []
        for asset_ids_item_data in self.asset_ids:
            asset_ids_item = str(asset_ids_item_data)
            asset_ids.append(asset_ids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "albumIds": album_ids,
                "assetIds": asset_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        album_ids = []
        _album_ids = d.pop("albumIds")
        for album_ids_item_data in _album_ids:
            album_ids_item = UUID(album_ids_item_data)

            album_ids.append(album_ids_item)

        asset_ids = []
        _asset_ids = d.pop("assetIds")
        for asset_ids_item_data in _asset_ids:
            asset_ids_item = UUID(asset_ids_item_data)

            asset_ids.append(asset_ids_item)

        albums_add_assets_dto = cls(
            album_ids=album_ids,
            asset_ids=asset_ids,
        )

        albums_add_assets_dto.additional_properties = d
        return albums_add_assets_dto

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
