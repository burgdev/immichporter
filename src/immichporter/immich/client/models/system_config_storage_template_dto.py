from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SystemConfigStorageTemplateDto")


@_attrs_define
class SystemConfigStorageTemplateDto:
    """
    Attributes:
        enabled (bool):
        hash_verification_enabled (bool):
        template (str):
    """

    enabled: bool
    hash_verification_enabled: bool
    template: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        hash_verification_enabled = self.hash_verification_enabled

        template = self.template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "hashVerificationEnabled": hash_verification_enabled,
                "template": template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        hash_verification_enabled = d.pop("hashVerificationEnabled")

        template = d.pop("template")

        system_config_storage_template_dto = cls(
            enabled=enabled,
            hash_verification_enabled=hash_verification_enabled,
            template=template,
        )

        system_config_storage_template_dto.additional_properties = d
        return system_config_storage_template_dto

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
