from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.system_config_smtp_dto import SystemConfigSmtpDto


T = TypeVar("T", bound="SystemConfigNotificationsDto")


@_attrs_define
class SystemConfigNotificationsDto:
    """
    Attributes:
        smtp (SystemConfigSmtpDto):
    """

    smtp: "SystemConfigSmtpDto"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        smtp = self.smtp.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "smtp": smtp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.system_config_smtp_dto import SystemConfigSmtpDto

        d = dict(src_dict)
        smtp = SystemConfigSmtpDto.from_dict(d.pop("smtp"))

        system_config_notifications_dto = cls(
            smtp=smtp,
        )

        system_config_notifications_dto.additional_properties = d
        return system_config_notifications_dto

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
