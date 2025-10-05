from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.image_format import ImageFormat

T = TypeVar("T", bound="SystemConfigGeneratedFullsizeImageDto")


@_attrs_define
class SystemConfigGeneratedFullsizeImageDto:
    """
    Attributes:
        enabled (bool):
        format_ (ImageFormat):
        quality (int):
    """

    enabled: bool
    format_: ImageFormat
    quality: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        format_ = self.format_.value

        quality = self.quality

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "format": format_,
                "quality": quality,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        format_ = ImageFormat(d.pop("format"))

        quality = d.pop("quality")

        system_config_generated_fullsize_image_dto = cls(
            enabled=enabled,
            format_=format_,
            quality=quality,
        )

        system_config_generated_fullsize_image_dto.additional_properties = d
        return system_config_generated_fullsize_image_dto

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
