from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.system_config_template_emails_dto import SystemConfigTemplateEmailsDto


T = TypeVar("T", bound="SystemConfigTemplatesDto")


@_attrs_define
class SystemConfigTemplatesDto:
    """
    Attributes:
        email (SystemConfigTemplateEmailsDto):
    """

    email: "SystemConfigTemplateEmailsDto"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.system_config_template_emails_dto import (
            SystemConfigTemplateEmailsDto,
        )

        d = dict(src_dict)
        email = SystemConfigTemplateEmailsDto.from_dict(d.pop("email"))

        system_config_templates_dto = cls(
            email=email,
        )

        system_config_templates_dto.additional_properties = d
        return system_config_templates_dto

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
