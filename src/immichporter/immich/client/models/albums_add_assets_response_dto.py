from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bulk_id_error_reason import BulkIdErrorReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="AlbumsAddAssetsResponseDto")


@_attrs_define
class AlbumsAddAssetsResponseDto:
    """
    Attributes:
        success (bool):
        error (Union[Unset, BulkIdErrorReason]):
    """

    success: bool
    error: Union[Unset, BulkIdErrorReason] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        error: Union[Unset, str] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success")

        _error = d.pop("error", UNSET)
        error: Union[Unset, BulkIdErrorReason]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = BulkIdErrorReason(_error)

        albums_add_assets_response_dto = cls(
            success=success,
            error=error,
        )

        albums_add_assets_response_dto.additional_properties = d
        return albums_add_assets_response_dto

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
