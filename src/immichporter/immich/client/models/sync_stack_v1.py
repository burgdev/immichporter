import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SyncStackV1")


@_attrs_define
class SyncStackV1:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        owner_id (str):
        primary_asset_id (str):
        updated_at (datetime.datetime):
    """

    created_at: datetime.datetime
    id: str
    owner_id: str
    primary_asset_id: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        owner_id = self.owner_id

        primary_asset_id = self.primary_asset_id

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "id": id,
                "ownerId": owner_id,
                "primaryAssetId": primary_asset_id,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("createdAt"))

        id = d.pop("id")

        owner_id = d.pop("ownerId")

        primary_asset_id = d.pop("primaryAssetId")

        updated_at = isoparse(d.pop("updatedAt"))

        sync_stack_v1 = cls(
            created_at=created_at,
            id=id,
            owner_id=owner_id,
            primary_asset_id=primary_asset_id,
            updated_at=updated_at,
        )

        sync_stack_v1.additional_properties = d
        return sync_stack_v1

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
