from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SystemConfigTemplateStorageOptionDto")


@_attrs_define
class SystemConfigTemplateStorageOptionDto:
    """
    Attributes:
        day_options (list[str]):
        hour_options (list[str]):
        minute_options (list[str]):
        month_options (list[str]):
        preset_options (list[str]):
        second_options (list[str]):
        week_options (list[str]):
        year_options (list[str]):
    """

    day_options: list[str]
    hour_options: list[str]
    minute_options: list[str]
    month_options: list[str]
    preset_options: list[str]
    second_options: list[str]
    week_options: list[str]
    year_options: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        day_options = self.day_options

        hour_options = self.hour_options

        minute_options = self.minute_options

        month_options = self.month_options

        preset_options = self.preset_options

        second_options = self.second_options

        week_options = self.week_options

        year_options = self.year_options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dayOptions": day_options,
                "hourOptions": hour_options,
                "minuteOptions": minute_options,
                "monthOptions": month_options,
                "presetOptions": preset_options,
                "secondOptions": second_options,
                "weekOptions": week_options,
                "yearOptions": year_options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        day_options = cast(list[str], d.pop("dayOptions"))

        hour_options = cast(list[str], d.pop("hourOptions"))

        minute_options = cast(list[str], d.pop("minuteOptions"))

        month_options = cast(list[str], d.pop("monthOptions"))

        preset_options = cast(list[str], d.pop("presetOptions"))

        second_options = cast(list[str], d.pop("secondOptions"))

        week_options = cast(list[str], d.pop("weekOptions"))

        year_options = cast(list[str], d.pop("yearOptions"))

        system_config_template_storage_option_dto = cls(
            day_options=day_options,
            hour_options=hour_options,
            minute_options=minute_options,
            month_options=month_options,
            preset_options=preset_options,
            second_options=second_options,
            week_options=week_options,
            year_options=year_options,
        )

        system_config_template_storage_option_dto.additional_properties = d
        return system_config_template_storage_option_dto

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
