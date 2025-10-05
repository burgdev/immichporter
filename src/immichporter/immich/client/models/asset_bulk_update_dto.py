from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_visibility import AssetVisibility
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssetBulkUpdateDto")


@_attrs_define
class AssetBulkUpdateDto:
    """
    Attributes:
        ids (list[UUID]):
        date_time_original (Union[Unset, str]):
        date_time_relative (Union[Unset, float]):
        description (Union[Unset, str]):
        duplicate_id (Union[None, Unset, str]):
        is_favorite (Union[Unset, bool]):
        latitude (Union[Unset, float]):
        longitude (Union[Unset, float]):
        rating (Union[Unset, float]):
        time_zone (Union[Unset, str]):
        visibility (Union[Unset, AssetVisibility]):
    """

    ids: list[UUID]
    date_time_original: Union[Unset, str] = UNSET
    date_time_relative: Union[Unset, float] = UNSET
    description: Union[Unset, str] = UNSET
    duplicate_id: Union[None, Unset, str] = UNSET
    is_favorite: Union[Unset, bool] = UNSET
    latitude: Union[Unset, float] = UNSET
    longitude: Union[Unset, float] = UNSET
    rating: Union[Unset, float] = UNSET
    time_zone: Union[Unset, str] = UNSET
    visibility: Union[Unset, AssetVisibility] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ids = []
        for ids_item_data in self.ids:
            ids_item = str(ids_item_data)
            ids.append(ids_item)

        date_time_original = self.date_time_original

        date_time_relative = self.date_time_relative

        description = self.description

        duplicate_id: Union[None, Unset, str]
        if isinstance(self.duplicate_id, Unset):
            duplicate_id = UNSET
        else:
            duplicate_id = self.duplicate_id

        is_favorite = self.is_favorite

        latitude = self.latitude

        longitude = self.longitude

        rating = self.rating

        time_zone = self.time_zone

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ids": ids,
            }
        )
        if date_time_original is not UNSET:
            field_dict["dateTimeOriginal"] = date_time_original
        if date_time_relative is not UNSET:
            field_dict["dateTimeRelative"] = date_time_relative
        if description is not UNSET:
            field_dict["description"] = description
        if duplicate_id is not UNSET:
            field_dict["duplicateId"] = duplicate_id
        if is_favorite is not UNSET:
            field_dict["isFavorite"] = is_favorite
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if rating is not UNSET:
            field_dict["rating"] = rating
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ids = []
        _ids = d.pop("ids")
        for ids_item_data in _ids:
            ids_item = UUID(ids_item_data)

            ids.append(ids_item)

        date_time_original = d.pop("dateTimeOriginal", UNSET)

        date_time_relative = d.pop("dateTimeRelative", UNSET)

        description = d.pop("description", UNSET)

        def _parse_duplicate_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        duplicate_id = _parse_duplicate_id(d.pop("duplicateId", UNSET))

        is_favorite = d.pop("isFavorite", UNSET)

        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        rating = d.pop("rating", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, AssetVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = AssetVisibility(_visibility)

        asset_bulk_update_dto = cls(
            ids=ids,
            date_time_original=date_time_original,
            date_time_relative=date_time_relative,
            description=description,
            duplicate_id=duplicate_id,
            is_favorite=is_favorite,
            latitude=latitude,
            longitude=longitude,
            rating=rating,
            time_zone=time_zone,
            visibility=visibility,
        )

        asset_bulk_update_dto.additional_properties = d
        return asset_bulk_update_dto

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
