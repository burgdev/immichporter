from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OAuthCallbackDto")


@_attrs_define
class OAuthCallbackDto:
    """
    Attributes:
        url (str):
        code_verifier (Union[Unset, str]):
        state (Union[Unset, str]):
    """

    url: str
    code_verifier: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        code_verifier = self.code_verifier

        state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if code_verifier is not UNSET:
            field_dict["codeVerifier"] = code_verifier
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        code_verifier = d.pop("codeVerifier", UNSET)

        state = d.pop("state", UNSET)

        o_auth_callback_dto = cls(
            url=url,
            code_verifier=code_verifier,
            state=state,
        )

        o_auth_callback_dto.additional_properties = d
        return o_auth_callback_dto

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
