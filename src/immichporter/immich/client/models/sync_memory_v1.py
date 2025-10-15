import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.memory_type import MemoryType

if TYPE_CHECKING:
    from ..models.sync_memory_v1_data import SyncMemoryV1Data


T = TypeVar("T", bound="SyncMemoryV1")


@_attrs_define
class SyncMemoryV1:
    """
    Attributes:
        created_at (datetime.datetime):
        data (SyncMemoryV1Data):
        deleted_at (Union[None, datetime.datetime]):
        hide_at (Union[None, datetime.datetime]):
        id (str):
        is_saved (bool):
        memory_at (datetime.datetime):
        owner_id (str):
        seen_at (Union[None, datetime.datetime]):
        show_at (Union[None, datetime.datetime]):
        type_ (MemoryType):
        updated_at (datetime.datetime):
    """

    created_at: datetime.datetime
    data: "SyncMemoryV1Data"
    deleted_at: Union[None, datetime.datetime]
    hide_at: Union[None, datetime.datetime]
    id: str
    is_saved: bool
    memory_at: datetime.datetime
    owner_id: str
    seen_at: Union[None, datetime.datetime]
    show_at: Union[None, datetime.datetime]
    type_: MemoryType
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        data = self.data.to_dict()

        deleted_at: Union[None, str]
        if isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        hide_at: Union[None, str]
        if isinstance(self.hide_at, datetime.datetime):
            hide_at = self.hide_at.isoformat()
        else:
            hide_at = self.hide_at

        id = self.id

        is_saved = self.is_saved

        memory_at = self.memory_at.isoformat()

        owner_id = self.owner_id

        seen_at: Union[None, str]
        if isinstance(self.seen_at, datetime.datetime):
            seen_at = self.seen_at.isoformat()
        else:
            seen_at = self.seen_at

        show_at: Union[None, str]
        if isinstance(self.show_at, datetime.datetime):
            show_at = self.show_at.isoformat()
        else:
            show_at = self.show_at

        type_ = self.type_.value

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "data": data,
                "deletedAt": deleted_at,
                "hideAt": hide_at,
                "id": id,
                "isSaved": is_saved,
                "memoryAt": memory_at,
                "ownerId": owner_id,
                "seenAt": seen_at,
                "showAt": show_at,
                "type": type_,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sync_memory_v1_data import SyncMemoryV1Data

        d = dict(src_dict)
        created_at = isoparse(d.pop("createdAt"))

        data = SyncMemoryV1Data.from_dict(d.pop("data"))

        def _parse_deleted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deleted_at = _parse_deleted_at(d.pop("deletedAt"))

        def _parse_hide_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                hide_at_type_0 = isoparse(data)

                return hide_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        hide_at = _parse_hide_at(d.pop("hideAt"))

        id = d.pop("id")

        is_saved = d.pop("isSaved")

        memory_at = isoparse(d.pop("memoryAt"))

        owner_id = d.pop("ownerId")

        def _parse_seen_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                seen_at_type_0 = isoparse(data)

                return seen_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        seen_at = _parse_seen_at(d.pop("seenAt"))

        def _parse_show_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                show_at_type_0 = isoparse(data)

                return show_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        show_at = _parse_show_at(d.pop("showAt"))

        type_ = MemoryType(d.pop("type"))

        updated_at = isoparse(d.pop("updatedAt"))

        sync_memory_v1 = cls(
            created_at=created_at,
            data=data,
            deleted_at=deleted_at,
            hide_at=hide_at,
            id=id,
            is_saved=is_saved,
            memory_at=memory_at,
            owner_id=owner_id,
            seen_at=seen_at,
            show_at=show_at,
            type_=type_,
            updated_at=updated_at,
        )

        sync_memory_v1.additional_properties = d
        return sync_memory_v1

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
