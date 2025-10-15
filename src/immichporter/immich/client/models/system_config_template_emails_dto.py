from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SystemConfigTemplateEmailsDto")


@_attrs_define
class SystemConfigTemplateEmailsDto:
    """
    Attributes:
        album_invite_template (str):
        album_update_template (str):
        welcome_template (str):
    """

    album_invite_template: str
    album_update_template: str
    welcome_template: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        album_invite_template = self.album_invite_template

        album_update_template = self.album_update_template

        welcome_template = self.welcome_template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "albumInviteTemplate": album_invite_template,
                "albumUpdateTemplate": album_update_template,
                "welcomeTemplate": welcome_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        album_invite_template = d.pop("albumInviteTemplate")

        album_update_template = d.pop("albumUpdateTemplate")

        welcome_template = d.pop("welcomeTemplate")

        system_config_template_emails_dto = cls(
            album_invite_template=album_invite_template,
            album_update_template=album_update_template,
            welcome_template=welcome_template,
        )

        system_config_template_emails_dto.additional_properties = d
        return system_config_template_emails_dto

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
