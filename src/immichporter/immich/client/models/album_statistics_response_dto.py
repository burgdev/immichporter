from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AlbumStatisticsResponseDto")


@_attrs_define
class AlbumStatisticsResponseDto:
    """
    Attributes:
        not_shared (int):
        owned (int):
        shared (int):
    """

    not_shared: int
    owned: int
    shared: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        not_shared = self.not_shared

        owned = self.owned

        shared = self.shared

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "notShared": not_shared,
                "owned": owned,
                "shared": shared,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        not_shared = d.pop("notShared")

        owned = d.pop("owned")

        shared = d.pop("shared")

        album_statistics_response_dto = cls(
            not_shared=not_shared,
            owned=owned,
            shared=shared,
        )

        album_statistics_response_dto.additional_properties = d
        return album_statistics_response_dto

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
