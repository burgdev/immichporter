from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionUnlockDto")


@_attrs_define
class SessionUnlockDto:
    """
    Attributes:
        password (Union[Unset, str]):
        pin_code (Union[Unset, str]):  Example: 123456.
    """

    password: Union[Unset, str] = UNSET
    pin_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        password = self.password

        pin_code = self.pin_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if password is not UNSET:
            field_dict["password"] = password
        if pin_code is not UNSET:
            field_dict["pinCode"] = pin_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        password = d.pop("password", UNSET)

        pin_code = d.pop("pinCode", UNSET)

        session_unlock_dto = cls(
            password=password,
            pin_code=pin_code,
        )

        session_unlock_dto.additional_properties = d
        return session_unlock_dto

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
