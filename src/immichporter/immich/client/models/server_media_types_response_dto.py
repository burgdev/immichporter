from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServerMediaTypesResponseDto")


@_attrs_define
class ServerMediaTypesResponseDto:
    """
    Attributes:
        image (list[str]):
        sidecar (list[str]):
        video (list[str]):
    """

    image: list[str]
    sidecar: list[str]
    video: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        sidecar = self.sidecar

        video = self.video

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "sidecar": sidecar,
                "video": video,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image = cast(list[str], d.pop("image"))

        sidecar = cast(list[str], d.pop("sidecar"))

        video = cast(list[str], d.pop("video"))

        server_media_types_response_dto = cls(
            image=image,
            sidecar=sidecar,
            video=video,
        )

        server_media_types_response_dto.additional_properties = d
        return server_media_types_response_dto

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
