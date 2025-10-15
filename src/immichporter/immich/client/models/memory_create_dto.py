import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.memory_type import MemoryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.on_this_day_dto import OnThisDayDto


T = TypeVar("T", bound="MemoryCreateDto")


@_attrs_define
class MemoryCreateDto:
    """
    Attributes:
        data (OnThisDayDto):
        memory_at (datetime.datetime):
        type_ (MemoryType):
        asset_ids (Union[Unset, list[UUID]]):
        is_saved (Union[Unset, bool]):
        seen_at (Union[Unset, datetime.datetime]):
    """

    data: "OnThisDayDto"
    memory_at: datetime.datetime
    type_: MemoryType
    asset_ids: Union[Unset, list[UUID]] = UNSET
    is_saved: Union[Unset, bool] = UNSET
    seen_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        memory_at = self.memory_at.isoformat()

        type_ = self.type_.value

        asset_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.asset_ids, Unset):
            asset_ids = []
            for asset_ids_item_data in self.asset_ids:
                asset_ids_item = str(asset_ids_item_data)
                asset_ids.append(asset_ids_item)

        is_saved = self.is_saved

        seen_at: Union[Unset, str] = UNSET
        if not isinstance(self.seen_at, Unset):
            seen_at = self.seen_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "memoryAt": memory_at,
                "type": type_,
            }
        )
        if asset_ids is not UNSET:
            field_dict["assetIds"] = asset_ids
        if is_saved is not UNSET:
            field_dict["isSaved"] = is_saved
        if seen_at is not UNSET:
            field_dict["seenAt"] = seen_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.on_this_day_dto import OnThisDayDto

        d = dict(src_dict)
        data = OnThisDayDto.from_dict(d.pop("data"))

        memory_at = isoparse(d.pop("memoryAt"))

        type_ = MemoryType(d.pop("type"))

        asset_ids = []
        _asset_ids = d.pop("assetIds", UNSET)
        for asset_ids_item_data in _asset_ids or []:
            asset_ids_item = UUID(asset_ids_item_data)

            asset_ids.append(asset_ids_item)

        is_saved = d.pop("isSaved", UNSET)

        _seen_at = d.pop("seenAt", UNSET)
        seen_at: Union[Unset, datetime.datetime]
        if isinstance(_seen_at, Unset):
            seen_at = UNSET
        else:
            seen_at = isoparse(_seen_at)

        memory_create_dto = cls(
            data=data,
            memory_at=memory_at,
            type_=type_,
            asset_ids=asset_ids,
            is_saved=is_saved,
            seen_at=seen_at,
        )

        memory_create_dto.additional_properties = d
        return memory_create_dto

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
