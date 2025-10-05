from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MachineLearningAvailabilityChecksDto")


@_attrs_define
class MachineLearningAvailabilityChecksDto:
    """
    Attributes:
        enabled (bool):
        interval (float):
        timeout (float):
    """

    enabled: bool
    interval: float
    timeout: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        interval = self.interval

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "interval": interval,
                "timeout": timeout,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        interval = d.pop("interval")

        timeout = d.pop("timeout")

        machine_learning_availability_checks_dto = cls(
            enabled=enabled,
            interval=interval,
            timeout=timeout,
        )

        machine_learning_availability_checks_dto.additional_properties = d
        return machine_learning_availability_checks_dto

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
