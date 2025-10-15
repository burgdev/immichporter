from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SystemConfigServerDto")


@_attrs_define
class SystemConfigServerDto:
    """
    Attributes:
        external_domain (str):
        login_page_message (str):
        public_users (bool):
    """

    external_domain: str
    login_page_message: str
    public_users: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        external_domain = self.external_domain

        login_page_message = self.login_page_message

        public_users = self.public_users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "externalDomain": external_domain,
                "loginPageMessage": login_page_message,
                "publicUsers": public_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        external_domain = d.pop("externalDomain")

        login_page_message = d.pop("loginPageMessage")

        public_users = d.pop("publicUsers")

        system_config_server_dto = cls(
            external_domain=external_domain,
            login_page_message=login_page_message,
            public_users=public_users,
        )

        system_config_server_dto.additional_properties = d
        return system_config_server_dto

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
