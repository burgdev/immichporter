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

T = TypeVar("T", bound="SyncPersonV1")


@_attrs_define
class SyncPersonV1:
    """
    Attributes:
        birth_date (Union[None, datetime.datetime]):
        color (Union[None, str]):
        created_at (datetime.datetime):
        face_asset_id (Union[None, str]):
        id (str):
        is_favorite (bool):
        is_hidden (bool):
        name (str):
        owner_id (str):
        updated_at (datetime.datetime):
    """

    birth_date: Union[None, datetime.datetime]
    color: Union[None, str]
    created_at: datetime.datetime
    face_asset_id: Union[None, str]
    id: str
    is_favorite: bool
    is_hidden: bool
    name: str
    owner_id: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        birth_date: Union[None, str]
        if isinstance(self.birth_date, datetime.datetime):
            birth_date = self.birth_date.isoformat()
        else:
            birth_date = self.birth_date

        color: Union[None, str]
        color = self.color

        created_at = self.created_at.isoformat()

        face_asset_id: Union[None, str]
        face_asset_id = self.face_asset_id

        id = self.id

        is_favorite = self.is_favorite

        is_hidden = self.is_hidden

        name = self.name

        owner_id = self.owner_id

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "birthDate": birth_date,
                "color": color,
                "createdAt": created_at,
                "faceAssetId": face_asset_id,
                "id": id,
                "isFavorite": is_favorite,
                "isHidden": is_hidden,
                "name": name,
                "ownerId": owner_id,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_birth_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birth_date_type_0 = isoparse(data)

                return birth_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        birth_date = _parse_birth_date(d.pop("birthDate"))

        def _parse_color(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        color = _parse_color(d.pop("color"))

        created_at = isoparse(d.pop("createdAt"))

        def _parse_face_asset_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        face_asset_id = _parse_face_asset_id(d.pop("faceAssetId"))

        id = d.pop("id")

        is_favorite = d.pop("isFavorite")

        is_hidden = d.pop("isHidden")

        name = d.pop("name")

        owner_id = d.pop("ownerId")

        updated_at = isoparse(d.pop("updatedAt"))

        sync_person_v1 = cls(
            birth_date=birth_date,
            color=color,
            created_at=created_at,
            face_asset_id=face_asset_id,
            id=id,
            is_favorite=is_favorite,
            is_hidden=is_hidden,
            name=name,
            owner_id=owner_id,
            updated_at=updated_at,
        )

        sync_person_v1.additional_properties = d
        return sync_person_v1

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
