from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TimeBucketsResponseDto")


@_attrs_define
class TimeBucketsResponseDto:
    """
    Attributes:
        count (int): Number of assets in this time bucket Example: 42.
        time_bucket (str): Time bucket identifier in YYYY-MM-DD format representing the start of the time period
            Example: 2024-01-01.
    """

    count: int
    time_bucket: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        time_bucket = self.time_bucket

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "timeBucket": time_bucket,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        time_bucket = d.pop("timeBucket")

        time_buckets_response_dto = cls(
            count=count,
            time_bucket=time_bucket,
        )

        time_buckets_response_dto.additional_properties = d
        return time_buckets_response_dto

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
