from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_metadata_key import UserMetadataKey

T = TypeVar("T", bound="SyncUserMetadataDeleteV1")


@_attrs_define
class SyncUserMetadataDeleteV1:
    """
    Attributes:
        key (UserMetadataKey):
        user_id (str):
    """

    key: UserMetadataKey
    user_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key.value

        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "userId": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = UserMetadataKey(d.pop("key"))

        user_id = d.pop("userId")

        sync_user_metadata_delete_v1 = cls(
            key=key,
            user_id=user_id,
        )

        sync_user_metadata_delete_v1.additional_properties = d
        return sync_user_metadata_delete_v1

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
