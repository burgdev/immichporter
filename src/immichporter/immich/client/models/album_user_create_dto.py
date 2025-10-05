from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.album_user_role import AlbumUserRole

T = TypeVar("T", bound="AlbumUserCreateDto")


@_attrs_define
class AlbumUserCreateDto:
    """
    Attributes:
        role (AlbumUserRole):
        user_id (UUID):
    """

    role: AlbumUserRole
    user_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role.value

        user_id = str(self.user_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "userId": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = AlbumUserRole(d.pop("role"))

        user_id = UUID(d.pop("userId"))

        album_user_create_dto = cls(
            role=role,
            user_id=user_id,
        )

        album_user_create_dto.additional_properties = d
        return album_user_create_dto

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
