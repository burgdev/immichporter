import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PersonCreateDto")


@_attrs_define
class PersonCreateDto:
    """
    Attributes:
        birth_date (Union[None, Unset, datetime.date]): Person date of birth.
            Note: the mobile app cannot currently set the birth date to null.
        color (Union[None, Unset, str]):
        is_favorite (Union[Unset, bool]):
        is_hidden (Union[Unset, bool]): Person visibility
        name (Union[Unset, str]): Person name.
    """

    birth_date: Union[None, Unset, datetime.date] = UNSET
    color: Union[None, Unset, str] = UNSET
    is_favorite: Union[Unset, bool] = UNSET
    is_hidden: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        birth_date: Union[None, Unset, str]
        if isinstance(self.birth_date, Unset):
            birth_date = UNSET
        elif isinstance(self.birth_date, datetime.date):
            birth_date = self.birth_date.isoformat()
        else:
            birth_date = self.birth_date

        color: Union[None, Unset, str]
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        is_favorite = self.is_favorite

        is_hidden = self.is_hidden

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if birth_date is not UNSET:
            field_dict["birthDate"] = birth_date
        if color is not UNSET:
            field_dict["color"] = color
        if is_favorite is not UNSET:
            field_dict["isFavorite"] = is_favorite
        if is_hidden is not UNSET:
            field_dict["isHidden"] = is_hidden
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_birth_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birth_date_type_0 = isoparse(data).date()

                return birth_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        birth_date = _parse_birth_date(d.pop("birthDate", UNSET))

        def _parse_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        color = _parse_color(d.pop("color", UNSET))

        is_favorite = d.pop("isFavorite", UNSET)

        is_hidden = d.pop("isHidden", UNSET)

        name = d.pop("name", UNSET)

        person_create_dto = cls(
            birth_date=birth_date,
            color=color,
            is_favorite=is_favorite,
            is_hidden=is_hidden,
            name=name,
        )

        person_create_dto.additional_properties = d
        return person_create_dto

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
