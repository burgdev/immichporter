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

T = TypeVar("T", bound="UserAdminUpdateDto")


@_attrs_define
class UserAdminUpdateDto:
    """
    Attributes:
        avatar_color (Union[None, Unset, UserAvatarColor]):
        email (Union[Unset, str]):
        is_admin (Union[Unset, bool]):
        name (Union[Unset, str]):
        password (Union[Unset, str]):
        pin_code (Union[None, Unset, str]):  Example: 123456.
        quota_size_in_bytes (Union[None, Unset, int]):
        should_change_password (Union[Unset, bool]):
        storage_label (Union[None, Unset, str]):
    """

    avatar_color: Union[None, Unset, UserAvatarColor] = UNSET
    email: Union[Unset, str] = UNSET
    is_admin: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    pin_code: Union[None, Unset, str] = UNSET
    quota_size_in_bytes: Union[None, Unset, int] = UNSET
    should_change_password: Union[Unset, bool] = UNSET
    storage_label: Union[None, Unset, str] = UNSET
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

        is_admin = self.is_admin

        name = self.name

        password = self.password

        pin_code: Union[None, Unset, str]
        if isinstance(self.pin_code, Unset):
            pin_code = UNSET
        else:
            pin_code = self.pin_code

        quota_size_in_bytes: Union[None, Unset, int]
        if isinstance(self.quota_size_in_bytes, Unset):
            quota_size_in_bytes = UNSET
        else:
            quota_size_in_bytes = self.quota_size_in_bytes

        should_change_password = self.should_change_password

        storage_label: Union[None, Unset, str]
        if isinstance(self.storage_label, Unset):
            storage_label = UNSET
        else:
            storage_label = self.storage_label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_color is not UNSET:
            field_dict["avatarColor"] = avatar_color
        if email is not UNSET:
            field_dict["email"] = email
        if is_admin is not UNSET:
            field_dict["isAdmin"] = is_admin
        if name is not UNSET:
            field_dict["name"] = name
        if password is not UNSET:
            field_dict["password"] = password
        if pin_code is not UNSET:
            field_dict["pinCode"] = pin_code
        if quota_size_in_bytes is not UNSET:
            field_dict["quotaSizeInBytes"] = quota_size_in_bytes
        if should_change_password is not UNSET:
            field_dict["shouldChangePassword"] = should_change_password
        if storage_label is not UNSET:
            field_dict["storageLabel"] = storage_label

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

        is_admin = d.pop("isAdmin", UNSET)

        name = d.pop("name", UNSET)

        password = d.pop("password", UNSET)

        def _parse_pin_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pin_code = _parse_pin_code(d.pop("pinCode", UNSET))

        def _parse_quota_size_in_bytes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        quota_size_in_bytes = _parse_quota_size_in_bytes(
            d.pop("quotaSizeInBytes", UNSET)
        )

        should_change_password = d.pop("shouldChangePassword", UNSET)

        def _parse_storage_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        storage_label = _parse_storage_label(d.pop("storageLabel", UNSET))

        user_admin_update_dto = cls(
            avatar_color=avatar_color,
            email=email,
            is_admin=is_admin,
            name=name,
            password=password,
            pin_code=pin_code,
            quota_size_in_bytes=quota_size_in_bytes,
            should_change_password=should_change_password,
            storage_label=storage_label,
        )

        user_admin_update_dto.additional_properties = d
        return user_admin_update_dto

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
