from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionCreateResponseDto")


@_attrs_define
class SessionCreateResponseDto:
    """
    Attributes:
        created_at (str):
        current (bool):
        device_os (str):
        device_type (str):
        id (str):
        is_pending_sync_reset (bool):
        token (str):
        updated_at (str):
        expires_at (Union[Unset, str]):
    """

    created_at: str
    current: bool
    device_os: str
    device_type: str
    id: str
    is_pending_sync_reset: bool
    token: str
    updated_at: str
    expires_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        current = self.current

        device_os = self.device_os

        device_type = self.device_type

        id = self.id

        is_pending_sync_reset = self.is_pending_sync_reset

        token = self.token

        updated_at = self.updated_at

        expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "current": current,
                "deviceOS": device_os,
                "deviceType": device_type,
                "id": id,
                "isPendingSyncReset": is_pending_sync_reset,
                "token": token,
                "updatedAt": updated_at,
            }
        )
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("createdAt")

        current = d.pop("current")

        device_os = d.pop("deviceOS")

        device_type = d.pop("deviceType")

        id = d.pop("id")

        is_pending_sync_reset = d.pop("isPendingSyncReset")

        token = d.pop("token")

        updated_at = d.pop("updatedAt")

        expires_at = d.pop("expiresAt", UNSET)

        session_create_response_dto = cls(
            created_at=created_at,
            current=current,
            device_os=device_os,
            device_type=device_type,
            id=id,
            is_pending_sync_reset=is_pending_sync_reset,
            token=token,
            updated_at=updated_at,
            expires_at=expires_at,
        )

        session_create_response_dto.additional_properties = d
        return session_create_response_dto

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
