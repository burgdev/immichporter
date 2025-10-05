from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SyncPartnerDeleteV1")


@_attrs_define
class SyncPartnerDeleteV1:
    """
    Attributes:
        shared_by_id (str):
        shared_with_id (str):
    """

    shared_by_id: str
    shared_with_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shared_by_id = self.shared_by_id

        shared_with_id = self.shared_with_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sharedById": shared_by_id,
                "sharedWithId": shared_with_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        shared_by_id = d.pop("sharedById")

        shared_with_id = d.pop("sharedWithId")

        sync_partner_delete_v1 = cls(
            shared_by_id=shared_by_id,
            shared_with_id=shared_with_id,
        )

        sync_partner_delete_v1.additional_properties = d
        return sync_partner_delete_v1

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
