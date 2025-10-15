from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VersionCheckStateResponseDto")


@_attrs_define
class VersionCheckStateResponseDto:
    """
    Attributes:
        checked_at (Union[None, str]):
        release_version (Union[None, str]):
    """

    checked_at: Union[None, str]
    release_version: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checked_at: Union[None, str]
        checked_at = self.checked_at

        release_version: Union[None, str]
        release_version = self.release_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checkedAt": checked_at,
                "releaseVersion": release_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_checked_at(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        checked_at = _parse_checked_at(d.pop("checkedAt"))

        def _parse_release_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        release_version = _parse_release_version(d.pop("releaseVersion"))

        version_check_state_response_dto = cls(
            checked_at=checked_at,
            release_version=release_version,
        )

        version_check_state_response_dto.additional_properties = d
        return version_check_state_response_dto

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
