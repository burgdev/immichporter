from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReverseGeocodingStateResponseDto")


@_attrs_define
class ReverseGeocodingStateResponseDto:
    """
    Attributes:
        last_import_file_name (Union[None, str]):
        last_update (Union[None, str]):
    """

    last_import_file_name: Union[None, str]
    last_update: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        last_import_file_name: Union[None, str]
        last_import_file_name = self.last_import_file_name

        last_update: Union[None, str]
        last_update = self.last_update

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lastImportFileName": last_import_file_name,
                "lastUpdate": last_update,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_last_import_file_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        last_import_file_name = _parse_last_import_file_name(
            d.pop("lastImportFileName")
        )

        def _parse_last_update(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        last_update = _parse_last_update(d.pop("lastUpdate"))

        reverse_geocoding_state_response_dto = cls(
            last_import_file_name=last_import_file_name,
            last_update=last_update,
        )

        reverse_geocoding_state_response_dto.additional_properties = d
        return reverse_geocoding_state_response_dto

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
