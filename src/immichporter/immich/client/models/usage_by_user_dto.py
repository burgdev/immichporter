from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UsageByUserDto")


@_attrs_define
class UsageByUserDto:
    """
    Attributes:
        photos (int):
        quota_size_in_bytes (Union[None, int]):
        usage (int):
        usage_photos (int):
        usage_videos (int):
        user_id (str):
        user_name (str):
        videos (int):
    """

    photos: int
    quota_size_in_bytes: Union[None, int]
    usage: int
    usage_photos: int
    usage_videos: int
    user_id: str
    user_name: str
    videos: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        photos = self.photos

        quota_size_in_bytes: Union[None, int]
        quota_size_in_bytes = self.quota_size_in_bytes

        usage = self.usage

        usage_photos = self.usage_photos

        usage_videos = self.usage_videos

        user_id = self.user_id

        user_name = self.user_name

        videos = self.videos

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "photos": photos,
                "quotaSizeInBytes": quota_size_in_bytes,
                "usage": usage,
                "usagePhotos": usage_photos,
                "usageVideos": usage_videos,
                "userId": user_id,
                "userName": user_name,
                "videos": videos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        photos = d.pop("photos")

        def _parse_quota_size_in_bytes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        quota_size_in_bytes = _parse_quota_size_in_bytes(d.pop("quotaSizeInBytes"))

        usage = d.pop("usage")

        usage_photos = d.pop("usagePhotos")

        usage_videos = d.pop("usageVideos")

        user_id = d.pop("userId")

        user_name = d.pop("userName")

        videos = d.pop("videos")

        usage_by_user_dto = cls(
            photos=photos,
            quota_size_in_bytes=quota_size_in_bytes,
            usage=usage,
            usage_photos=usage_photos,
            usage_videos=usage_videos,
            user_id=user_id,
            user_name=user_name,
            videos=videos,
        )

        usage_by_user_dto.additional_properties = d
        return usage_by_user_dto

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
