from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OAuthConfigDto")


@_attrs_define
class OAuthConfigDto:
    """
    Attributes:
        redirect_uri (str):
        code_challenge (Union[Unset, str]):
        state (Union[Unset, str]):
    """

    redirect_uri: str
    code_challenge: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        redirect_uri = self.redirect_uri

        code_challenge = self.code_challenge

        state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "redirectUri": redirect_uri,
            }
        )
        if code_challenge is not UNSET:
            field_dict["codeChallenge"] = code_challenge
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        redirect_uri = d.pop("redirectUri")

        code_challenge = d.pop("codeChallenge", UNSET)

        state = d.pop("state", UNSET)

        o_auth_config_dto = cls(
            redirect_uri=redirect_uri,
            code_challenge=code_challenge,
            state=state,
        )

        o_auth_config_dto.additional_properties = d
        return o_auth_config_dto

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
