from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthStatusResponseDto")


@_attrs_define
class AuthStatusResponseDto:
    """
    Attributes:
        is_elevated (bool):
        password (bool):
        pin_code (bool):
        expires_at (Union[Unset, str]):
        pin_expires_at (Union[Unset, str]):
    """

    is_elevated: bool
    password: bool
    pin_code: bool
    expires_at: Union[Unset, str] = UNSET
    pin_expires_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_elevated = self.is_elevated

        password = self.password

        pin_code = self.pin_code

        expires_at = self.expires_at

        pin_expires_at = self.pin_expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "isElevated": is_elevated,
                "password": password,
                "pinCode": pin_code,
            }
        )
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if pin_expires_at is not UNSET:
            field_dict["pinExpiresAt"] = pin_expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_elevated = d.pop("isElevated")

        password = d.pop("password")

        pin_code = d.pop("pinCode")

        expires_at = d.pop("expiresAt", UNSET)

        pin_expires_at = d.pop("pinExpiresAt", UNSET)

        auth_status_response_dto = cls(
            is_elevated=is_elevated,
            password=password,
            pin_code=pin_code,
            expires_at=expires_at,
            pin_expires_at=pin_expires_at,
        )

        auth_status_response_dto.additional_properties = d
        return auth_status_response_dto

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
