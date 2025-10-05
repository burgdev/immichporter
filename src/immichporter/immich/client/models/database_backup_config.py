from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DatabaseBackupConfig")


@_attrs_define
class DatabaseBackupConfig:
    """
    Attributes:
        cron_expression (str):
        enabled (bool):
        keep_last_amount (float):
    """

    cron_expression: str
    enabled: bool
    keep_last_amount: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cron_expression = self.cron_expression

        enabled = self.enabled

        keep_last_amount = self.keep_last_amount

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cronExpression": cron_expression,
                "enabled": enabled,
                "keepLastAmount": keep_last_amount,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cron_expression = d.pop("cronExpression")

        enabled = d.pop("enabled")

        keep_last_amount = d.pop("keepLastAmount")

        database_backup_config = cls(
            cron_expression=cron_expression,
            enabled=enabled,
            keep_last_amount=keep_last_amount,
        )

        database_backup_config.additional_properties = d
        return database_backup_config

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
