from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.o_auth_token_endpoint_auth_method import OAuthTokenEndpointAuthMethod

T = TypeVar("T", bound="SystemConfigOAuthDto")


@_attrs_define
class SystemConfigOAuthDto:
    """
    Attributes:
        auto_launch (bool):
        auto_register (bool):
        button_text (str):
        client_id (str):
        client_secret (str):
        default_storage_quota (Union[None, int]):
        enabled (bool):
        issuer_url (str):
        mobile_override_enabled (bool):
        mobile_redirect_uri (str):
        profile_signing_algorithm (str):
        role_claim (str):
        scope (str):
        signing_algorithm (str):
        storage_label_claim (str):
        storage_quota_claim (str):
        timeout (int):
        token_endpoint_auth_method (OAuthTokenEndpointAuthMethod):
    """

    auto_launch: bool
    auto_register: bool
    button_text: str
    client_id: str
    client_secret: str
    default_storage_quota: Union[None, int]
    enabled: bool
    issuer_url: str
    mobile_override_enabled: bool
    mobile_redirect_uri: str
    profile_signing_algorithm: str
    role_claim: str
    scope: str
    signing_algorithm: str
    storage_label_claim: str
    storage_quota_claim: str
    timeout: int
    token_endpoint_auth_method: OAuthTokenEndpointAuthMethod
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auto_launch = self.auto_launch

        auto_register = self.auto_register

        button_text = self.button_text

        client_id = self.client_id

        client_secret = self.client_secret

        default_storage_quota: Union[None, int]
        default_storage_quota = self.default_storage_quota

        enabled = self.enabled

        issuer_url = self.issuer_url

        mobile_override_enabled = self.mobile_override_enabled

        mobile_redirect_uri = self.mobile_redirect_uri

        profile_signing_algorithm = self.profile_signing_algorithm

        role_claim = self.role_claim

        scope = self.scope

        signing_algorithm = self.signing_algorithm

        storage_label_claim = self.storage_label_claim

        storage_quota_claim = self.storage_quota_claim

        timeout = self.timeout

        token_endpoint_auth_method = self.token_endpoint_auth_method.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "autoLaunch": auto_launch,
                "autoRegister": auto_register,
                "buttonText": button_text,
                "clientId": client_id,
                "clientSecret": client_secret,
                "defaultStorageQuota": default_storage_quota,
                "enabled": enabled,
                "issuerUrl": issuer_url,
                "mobileOverrideEnabled": mobile_override_enabled,
                "mobileRedirectUri": mobile_redirect_uri,
                "profileSigningAlgorithm": profile_signing_algorithm,
                "roleClaim": role_claim,
                "scope": scope,
                "signingAlgorithm": signing_algorithm,
                "storageLabelClaim": storage_label_claim,
                "storageQuotaClaim": storage_quota_claim,
                "timeout": timeout,
                "tokenEndpointAuthMethod": token_endpoint_auth_method,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auto_launch = d.pop("autoLaunch")

        auto_register = d.pop("autoRegister")

        button_text = d.pop("buttonText")

        client_id = d.pop("clientId")

        client_secret = d.pop("clientSecret")

        def _parse_default_storage_quota(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        default_storage_quota = _parse_default_storage_quota(
            d.pop("defaultStorageQuota")
        )

        enabled = d.pop("enabled")

        issuer_url = d.pop("issuerUrl")

        mobile_override_enabled = d.pop("mobileOverrideEnabled")

        mobile_redirect_uri = d.pop("mobileRedirectUri")

        profile_signing_algorithm = d.pop("profileSigningAlgorithm")

        role_claim = d.pop("roleClaim")

        scope = d.pop("scope")

        signing_algorithm = d.pop("signingAlgorithm")

        storage_label_claim = d.pop("storageLabelClaim")

        storage_quota_claim = d.pop("storageQuotaClaim")

        timeout = d.pop("timeout")

        token_endpoint_auth_method = OAuthTokenEndpointAuthMethod(
            d.pop("tokenEndpointAuthMethod")
        )

        system_config_o_auth_dto = cls(
            auto_launch=auto_launch,
            auto_register=auto_register,
            button_text=button_text,
            client_id=client_id,
            client_secret=client_secret,
            default_storage_quota=default_storage_quota,
            enabled=enabled,
            issuer_url=issuer_url,
            mobile_override_enabled=mobile_override_enabled,
            mobile_redirect_uri=mobile_redirect_uri,
            profile_signing_algorithm=profile_signing_algorithm,
            role_claim=role_claim,
            scope=scope,
            signing_algorithm=signing_algorithm,
            storage_label_claim=storage_label_claim,
            storage_quota_claim=storage_quota_claim,
            timeout=timeout,
            token_endpoint_auth_method=token_endpoint_auth_method,
        )

        system_config_o_auth_dto.additional_properties = d
        return system_config_o_auth_dto

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
