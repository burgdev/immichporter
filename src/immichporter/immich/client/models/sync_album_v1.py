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

from ..models.asset_order import AssetOrder

T = TypeVar("T", bound="SyncAlbumV1")


@_attrs_define
class SyncAlbumV1:
    """
    Attributes:
        created_at (datetime.datetime):
        description (str):
        id (str):
        is_activity_enabled (bool):
        name (str):
        order (AssetOrder):
        owner_id (str):
        thumbnail_asset_id (Union[None, str]):
        updated_at (datetime.datetime):
    """

    created_at: datetime.datetime
    description: str
    id: str
    is_activity_enabled: bool
    name: str
    order: AssetOrder
    owner_id: str
    thumbnail_asset_id: Union[None, str]
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        description = self.description

        id = self.id

        is_activity_enabled = self.is_activity_enabled

        name = self.name

        order = self.order.value

        owner_id = self.owner_id

        thumbnail_asset_id: Union[None, str]
        thumbnail_asset_id = self.thumbnail_asset_id

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "description": description,
                "id": id,
                "isActivityEnabled": is_activity_enabled,
                "name": name,
                "order": order,
                "ownerId": owner_id,
                "thumbnailAssetId": thumbnail_asset_id,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("createdAt"))

        description = d.pop("description")

        id = d.pop("id")

        is_activity_enabled = d.pop("isActivityEnabled")

        name = d.pop("name")

        order = AssetOrder(d.pop("order"))

        owner_id = d.pop("ownerId")

        def _parse_thumbnail_asset_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        thumbnail_asset_id = _parse_thumbnail_asset_id(d.pop("thumbnailAssetId"))

        updated_at = isoparse(d.pop("updatedAt"))

        sync_album_v1 = cls(
            created_at=created_at,
            description=description,
            id=id,
            is_activity_enabled=is_activity_enabled,
            name=name,
            order=order,
            owner_id=owner_id,
            thumbnail_asset_id=thumbnail_asset_id,
            updated_at=updated_at,
        )

        sync_album_v1.additional_properties = d
        return sync_album_v1

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
