import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.notification_level import NotificationLevel
from ..models.notification_type import NotificationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notification_dto_data import NotificationDtoData


T = TypeVar("T", bound="NotificationDto")


@_attrs_define
class NotificationDto:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        level (NotificationLevel):
        title (str):
        type_ (NotificationType):
        data (Union[Unset, NotificationDtoData]):
        description (Union[Unset, str]):
        read_at (Union[Unset, datetime.datetime]):
    """

    created_at: datetime.datetime
    id: str
    level: NotificationLevel
    title: str
    type_: NotificationType
    data: Union[Unset, "NotificationDtoData"] = UNSET
    description: Union[Unset, str] = UNSET
    read_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        level = self.level.value

        title = self.title

        type_ = self.type_.value

        data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        description = self.description

        read_at: Union[Unset, str] = UNSET
        if not isinstance(self.read_at, Unset):
            read_at = self.read_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "id": id,
                "level": level,
                "title": title,
                "type": type_,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data
        if description is not UNSET:
            field_dict["description"] = description
        if read_at is not UNSET:
            field_dict["readAt"] = read_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification_dto_data import NotificationDtoData

        d = dict(src_dict)
        created_at = isoparse(d.pop("createdAt"))

        id = d.pop("id")

        level = NotificationLevel(d.pop("level"))

        title = d.pop("title")

        type_ = NotificationType(d.pop("type"))

        _data = d.pop("data", UNSET)
        data: Union[Unset, NotificationDtoData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = NotificationDtoData.from_dict(_data)

        description = d.pop("description", UNSET)

        _read_at = d.pop("readAt", UNSET)
        read_at: Union[Unset, datetime.datetime]
        if isinstance(_read_at, Unset):
            read_at = UNSET
        else:
            read_at = isoparse(_read_at)

        notification_dto = cls(
            created_at=created_at,
            id=id,
            level=level,
            title=title,
            type_=type_,
            data=data,
            description=description,
            read_at=read_at,
        )

        notification_dto.additional_properties = d
        return notification_dto

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
