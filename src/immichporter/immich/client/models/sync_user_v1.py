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

from ..models.user_avatar_color import UserAvatarColor

T = TypeVar("T", bound="SyncUserV1")


@_attrs_define
class SyncUserV1:
    """
    Attributes:
        avatar_color (Union[None, UserAvatarColor]):
        deleted_at (Union[None, datetime.datetime]):
        email (str):
        has_profile_image (bool):
        id (str):
        name (str):
        profile_changed_at (datetime.datetime):
    """

    avatar_color: Union[None, UserAvatarColor]
    deleted_at: Union[None, datetime.datetime]
    email: str
    has_profile_image: bool
    id: str
    name: str
    profile_changed_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_color: Union[None, str]
        if isinstance(self.avatar_color, UserAvatarColor):
            avatar_color = self.avatar_color.value
        else:
            avatar_color = self.avatar_color

        deleted_at: Union[None, str]
        if isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        email = self.email

        has_profile_image = self.has_profile_image

        id = self.id

        name = self.name

        profile_changed_at = self.profile_changed_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "avatarColor": avatar_color,
                "deletedAt": deleted_at,
                "email": email,
                "hasProfileImage": has_profile_image,
                "id": id,
                "name": name,
                "profileChangedAt": profile_changed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_avatar_color(data: object) -> Union[None, UserAvatarColor]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                avatar_color_type_1 = UserAvatarColor(data)

                return avatar_color_type_1
            except:  # noqa: E722
                pass
            return cast(Union[None, UserAvatarColor], data)

        avatar_color = _parse_avatar_color(d.pop("avatarColor"))

        def _parse_deleted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deleted_at = _parse_deleted_at(d.pop("deletedAt"))

        email = d.pop("email")

        has_profile_image = d.pop("hasProfileImage")

        id = d.pop("id")

        name = d.pop("name")

        profile_changed_at = isoparse(d.pop("profileChangedAt"))

        sync_user_v1 = cls(
            avatar_color=avatar_color,
            deleted_at=deleted_at,
            email=email,
            has_profile_image=has_profile_image,
            id=id,
            name=name,
            profile_changed_at=profile_changed_at,
        )

        sync_user_v1.additional_properties = d
        return sync_user_v1

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
