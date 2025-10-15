from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SyncAssetFaceV1")


@_attrs_define
class SyncAssetFaceV1:
    """
    Attributes:
        asset_id (str):
        bounding_box_x1 (int):
        bounding_box_x2 (int):
        bounding_box_y1 (int):
        bounding_box_y2 (int):
        id (str):
        image_height (int):
        image_width (int):
        person_id (Union[None, str]):
        source_type (str):
    """

    asset_id: str
    bounding_box_x1: int
    bounding_box_x2: int
    bounding_box_y1: int
    bounding_box_y2: int
    id: str
    image_height: int
    image_width: int
    person_id: Union[None, str]
    source_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_id = self.asset_id

        bounding_box_x1 = self.bounding_box_x1

        bounding_box_x2 = self.bounding_box_x2

        bounding_box_y1 = self.bounding_box_y1

        bounding_box_y2 = self.bounding_box_y2

        id = self.id

        image_height = self.image_height

        image_width = self.image_width

        person_id: Union[None, str]
        person_id = self.person_id

        source_type = self.source_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assetId": asset_id,
                "boundingBoxX1": bounding_box_x1,
                "boundingBoxX2": bounding_box_x2,
                "boundingBoxY1": bounding_box_y1,
                "boundingBoxY2": bounding_box_y2,
                "id": id,
                "imageHeight": image_height,
                "imageWidth": image_width,
                "personId": person_id,
                "sourceType": source_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_id = d.pop("assetId")

        bounding_box_x1 = d.pop("boundingBoxX1")

        bounding_box_x2 = d.pop("boundingBoxX2")

        bounding_box_y1 = d.pop("boundingBoxY1")

        bounding_box_y2 = d.pop("boundingBoxY2")

        id = d.pop("id")

        image_height = d.pop("imageHeight")

        image_width = d.pop("imageWidth")

        def _parse_person_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        person_id = _parse_person_id(d.pop("personId"))

        source_type = d.pop("sourceType")

        sync_asset_face_v1 = cls(
            asset_id=asset_id,
            bounding_box_x1=bounding_box_x1,
            bounding_box_x2=bounding_box_x2,
            bounding_box_y1=bounding_box_y1,
            bounding_box_y2=bounding_box_y2,
            id=id,
            image_height=image_height,
            image_width=image_width,
            person_id=person_id,
            source_type=source_type,
        )

        sync_asset_face_v1.additional_properties = d
        return sync_asset_face_v1

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
