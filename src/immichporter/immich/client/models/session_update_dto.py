from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionUpdateDto")


@_attrs_define
class SessionUpdateDto:
    """
    Attributes:
        is_pending_sync_reset (Union[Unset, bool]):
    """

    is_pending_sync_reset: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_pending_sync_reset = self.is_pending_sync_reset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_pending_sync_reset is not UNSET:
            field_dict["isPendingSyncReset"] = is_pending_sync_reset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_pending_sync_reset = d.pop("isPendingSyncReset", UNSET)

        session_update_dto = cls(
            is_pending_sync_reset=is_pending_sync_reset,
        )

        session_update_dto.additional_properties = d
        return session_update_dto

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
