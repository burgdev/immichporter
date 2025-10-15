from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateLibraryDto")


@_attrs_define
class UpdateLibraryDto:
    """
    Attributes:
        exclusion_patterns (Union[Unset, list[str]]):
        import_paths (Union[Unset, list[str]]):
        name (Union[Unset, str]):
    """

    exclusion_patterns: Union[Unset, list[str]] = UNSET
    import_paths: Union[Unset, list[str]] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exclusion_patterns: Union[Unset, list[str]] = UNSET
        if not isinstance(self.exclusion_patterns, Unset):
            exclusion_patterns = self.exclusion_patterns

        import_paths: Union[Unset, list[str]] = UNSET
        if not isinstance(self.import_paths, Unset):
            import_paths = self.import_paths

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if exclusion_patterns is not UNSET:
            field_dict["exclusionPatterns"] = exclusion_patterns
        if import_paths is not UNSET:
            field_dict["importPaths"] = import_paths
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exclusion_patterns = cast(list[str], d.pop("exclusionPatterns", UNSET))

        import_paths = cast(list[str], d.pop("importPaths", UNSET))

        name = d.pop("name", UNSET)

        update_library_dto = cls(
            exclusion_patterns=exclusion_patterns,
            import_paths=import_paths,
            name=name,
        )

        update_library_dto.additional_properties = d
        return update_library_dto

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
