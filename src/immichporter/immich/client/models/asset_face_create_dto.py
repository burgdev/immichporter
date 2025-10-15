from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AssetFaceCreateDto")


@_attrs_define
class AssetFaceCreateDto:
    """
    Attributes:
        asset_id (UUID):
        height (int):
        image_height (int):
        image_width (int):
        person_id (UUID):
        width (int):
        x (int):
        y (int):
    """

    asset_id: UUID
    height: int
    image_height: int
    image_width: int
    person_id: UUID
    width: int
    x: int
    y: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_id = str(self.asset_id)

        height = self.height

        image_height = self.image_height

        image_width = self.image_width

        person_id = str(self.person_id)

        width = self.width

        x = self.x

        y = self.y

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assetId": asset_id,
                "height": height,
                "imageHeight": image_height,
                "imageWidth": image_width,
                "personId": person_id,
                "width": width,
                "x": x,
                "y": y,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_id = UUID(d.pop("assetId"))

        height = d.pop("height")

        image_height = d.pop("imageHeight")

        image_width = d.pop("imageWidth")

        person_id = UUID(d.pop("personId"))

        width = d.pop("width")

        x = d.pop("x")

        y = d.pop("y")

        asset_face_create_dto = cls(
            asset_id=asset_id,
            height=height,
            image_height=image_height,
            image_width=image_width,
            person_id=person_id,
            width=width,
            x=x,
            y=y,
        )

        asset_face_create_dto.additional_properties = d
        return asset_face_create_dto

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
