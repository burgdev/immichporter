from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_job_name import AssetJobName

T = TypeVar("T", bound="AssetJobsDto")


@_attrs_define
class AssetJobsDto:
    """
    Attributes:
        asset_ids (list[UUID]):
        name (AssetJobName):
    """

    asset_ids: list[UUID]
    name: AssetJobName
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_ids = []
        for asset_ids_item_data in self.asset_ids:
            asset_ids_item = str(asset_ids_item_data)
            asset_ids.append(asset_ids_item)

        name = self.name.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assetIds": asset_ids,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_ids = []
        _asset_ids = d.pop("assetIds")
        for asset_ids_item_data in _asset_ids:
            asset_ids_item = UUID(asset_ids_item_data)

            asset_ids.append(asset_ids_item)

        name = AssetJobName(d.pop("name"))

        asset_jobs_dto = cls(
            asset_ids=asset_ids,
            name=name,
        )

        asset_jobs_dto.additional_properties = d
        return asset_jobs_dto

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
