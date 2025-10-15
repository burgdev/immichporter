import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.notification_level import NotificationLevel
from ..models.notification_type import NotificationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notification_create_dto_data import NotificationCreateDtoData


T = TypeVar("T", bound="NotificationCreateDto")


@_attrs_define
class NotificationCreateDto:
    """
    Attributes:
        title (str):
        user_id (UUID):
        data (Union[Unset, NotificationCreateDtoData]):
        description (Union[None, Unset, str]):
        level (Union[Unset, NotificationLevel]):
        read_at (Union[None, Unset, datetime.datetime]):
        type_ (Union[Unset, NotificationType]):
    """

    title: str
    user_id: UUID
    data: Union[Unset, "NotificationCreateDtoData"] = UNSET
    description: Union[None, Unset, str] = UNSET
    level: Union[Unset, NotificationLevel] = UNSET
    read_at: Union[None, Unset, datetime.datetime] = UNSET
    type_: Union[Unset, NotificationType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        user_id = str(self.user_id)

        data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        level: Union[Unset, str] = UNSET
        if not isinstance(self.level, Unset):
            level = self.level.value

        read_at: Union[None, Unset, str]
        if isinstance(self.read_at, Unset):
            read_at = UNSET
        elif isinstance(self.read_at, datetime.datetime):
            read_at = self.read_at.isoformat()
        else:
            read_at = self.read_at

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "userId": user_id,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data
        if description is not UNSET:
            field_dict["description"] = description
        if level is not UNSET:
            field_dict["level"] = level
        if read_at is not UNSET:
            field_dict["readAt"] = read_at
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification_create_dto_data import NotificationCreateDtoData

        d = dict(src_dict)
        title = d.pop("title")

        user_id = UUID(d.pop("userId"))

        _data = d.pop("data", UNSET)
        data: Union[Unset, NotificationCreateDtoData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = NotificationCreateDtoData.from_dict(_data)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _level = d.pop("level", UNSET)
        level: Union[Unset, NotificationLevel]
        if isinstance(_level, Unset):
            level = UNSET
        else:
            level = NotificationLevel(_level)

        def _parse_read_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                read_at_type_0 = isoparse(data)

                return read_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        read_at = _parse_read_at(d.pop("readAt", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, NotificationType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = NotificationType(_type_)

        notification_create_dto = cls(
            title=title,
            user_id=user_id,
            data=data,
            description=description,
            level=level,
            read_at=read_at,
            type_=type_,
        )

        notification_create_dto.additional_properties = d
        return notification_create_dto

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
