from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServerApkLinksDto")


@_attrs_define
class ServerApkLinksDto:
    """
    Attributes:
        arm64v8a (str):
        armeabiv7a (str):
        universal (str):
        x86_64 (str):
    """

    arm64v8a: str
    armeabiv7a: str
    universal: str
    x86_64: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        arm64v8a = self.arm64v8a

        armeabiv7a = self.armeabiv7a

        universal = self.universal

        x86_64 = self.x86_64

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "arm64v8a": arm64v8a,
                "armeabiv7a": armeabiv7a,
                "universal": universal,
                "x86_64": x86_64,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        arm64v8a = d.pop("arm64v8a")

        armeabiv7a = d.pop("armeabiv7a")

        universal = d.pop("universal")

        x86_64 = d.pop("x86_64")

        server_apk_links_dto = cls(
            arm64v8a=arm64v8a,
            armeabiv7a=armeabiv7a,
            universal=universal,
            x86_64=x86_64,
        )

        server_apk_links_dto.additional_properties = d
        return server_apk_links_dto

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
