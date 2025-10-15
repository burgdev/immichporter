from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_avatar_color import UserAvatarColor
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserUpdateMeDto")


@_attrs_define
class UserUpdateMeDto:
    """
    Attributes:
        avatar_color (Union[None, Unset, UserAvatarColor]):
        email (Union[Unset, str]):
        name (Union[Unset, str]):
        password (Union[Unset, str]):
    """

    avatar_color: Union[None, Unset, UserAvatarColor] = UNSET
    email: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_color: Union[None, Unset, str]
        if isinstance(self.avatar_color, Unset):
            avatar_color = UNSET
        elif isinstance(self.avatar_color, UserAvatarColor):
            avatar_color = self.avatar_color.value
        else:
            avatar_color = self.avatar_color

        email = self.email

        name = self.name

        password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_color is not UNSET:
            field_dict["avatarColor"] = avatar_color
        if email is not UNSET:
            field_dict["email"] = email
        if name is not UNSET:
            field_dict["name"] = name
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_avatar_color(data: object) -> Union[None, Unset, UserAvatarColor]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                avatar_color_type_1 = UserAvatarColor(data)

                return avatar_color_type_1
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, UserAvatarColor], data)

        avatar_color = _parse_avatar_color(d.pop("avatarColor", UNSET))

        email = d.pop("email", UNSET)

        name = d.pop("name", UNSET)

        password = d.pop("password", UNSET)

        user_update_me_dto = cls(
            avatar_color=avatar_color,
            email=email,
            name=name,
            password=password,
        )

        user_update_me_dto.additional_properties = d
        return user_update_me_dto

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
