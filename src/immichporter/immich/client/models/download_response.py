from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DownloadResponse")


@_attrs_define
class DownloadResponse:
    """
    Attributes:
        archive_size (int):
        include_embedded_videos (bool):  Default: False.
    """

    archive_size: int
    include_embedded_videos: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        archive_size = self.archive_size

        include_embedded_videos = self.include_embedded_videos

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "archiveSize": archive_size,
                "includeEmbeddedVideos": include_embedded_videos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        archive_size = d.pop("archiveSize")

        include_embedded_videos = d.pop("includeEmbeddedVideos")

        download_response = cls(
            archive_size=archive_size,
            include_embedded_videos=include_embedded_videos,
        )

        download_response.additional_properties = d
        return download_response

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
