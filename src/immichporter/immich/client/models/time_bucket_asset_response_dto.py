from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_visibility import AssetVisibility
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeBucketAssetResponseDto")


@_attrs_define
class TimeBucketAssetResponseDto:
    """
    Attributes:
        city (list[Union[None, str]]): Array of city names extracted from EXIF GPS data
        country (list[Union[None, str]]): Array of country names extracted from EXIF GPS data
        duration (list[Union[None, str]]): Array of video durations in HH:MM:SS format (null for images)
        file_created_at (list[str]): Array of file creation timestamps in UTC (ISO 8601 format, without timezone)
        id (list[str]): Array of asset IDs in the time bucket
        is_favorite (list[bool]): Array indicating whether each asset is favorited
        is_image (list[bool]): Array indicating whether each asset is an image (false for videos)
        is_trashed (list[bool]): Array indicating whether each asset is in the trash
        live_photo_video_id (list[Union[None, str]]): Array of live photo video asset IDs (null for non-live photos)
        local_offset_hours (list[float]): Array of UTC offset hours at the time each photo was taken. Positive values
            are east of UTC, negative values are west of UTC. Values may be fractional (e.g., 5.5 for +05:30, -9.75 for
            -09:45). Applying this offset to 'fileCreatedAt' will give you the time the photo was taken from the
            photographer's perspective.
        owner_id (list[str]): Array of owner IDs for each asset
        projection_type (list[Union[None, str]]): Array of projection types for 360° content (e.g., "EQUIRECTANGULAR",
            "CUBEFACE", "CYLINDRICAL")
        ratio (list[float]): Array of aspect ratios (width/height) for each asset
        thumbhash (list[Union[None, str]]): Array of BlurHash strings for generating asset previews (base64 encoded)
        visibility (list[AssetVisibility]): Array of visibility statuses for each asset (e.g., ARCHIVE, TIMELINE,
            HIDDEN, LOCKED)
        latitude (Union[Unset, list[Union[None, float]]]): Array of latitude coordinates extracted from EXIF GPS data
        longitude (Union[Unset, list[Union[None, float]]]): Array of longitude coordinates extracted from EXIF GPS data
        stack (Union[Unset, list[Union[None, list[str]]]]): Array of stack information as [stackId, assetCount] tuples
            (null for non-stacked assets)
    """

    city: list[Union[None, str]]
    country: list[Union[None, str]]
    duration: list[Union[None, str]]
    file_created_at: list[str]
    id: list[str]
    is_favorite: list[bool]
    is_image: list[bool]
    is_trashed: list[bool]
    live_photo_video_id: list[Union[None, str]]
    local_offset_hours: list[float]
    owner_id: list[str]
    projection_type: list[Union[None, str]]
    ratio: list[float]
    thumbhash: list[Union[None, str]]
    visibility: list[AssetVisibility]
    latitude: Union[Unset, list[Union[None, float]]] = UNSET
    longitude: Union[Unset, list[Union[None, float]]] = UNSET
    stack: Union[Unset, list[Union[None, list[str]]]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        city = []
        for city_item_data in self.city:
            city_item: Union[None, str]
            city_item = city_item_data
            city.append(city_item)

        country = []
        for country_item_data in self.country:
            country_item: Union[None, str]
            country_item = country_item_data
            country.append(country_item)

        duration = []
        for duration_item_data in self.duration:
            duration_item: Union[None, str]
            duration_item = duration_item_data
            duration.append(duration_item)

        file_created_at = self.file_created_at

        id = self.id

        is_favorite = self.is_favorite

        is_image = self.is_image

        is_trashed = self.is_trashed

        live_photo_video_id = []
        for live_photo_video_id_item_data in self.live_photo_video_id:
            live_photo_video_id_item: Union[None, str]
            live_photo_video_id_item = live_photo_video_id_item_data
            live_photo_video_id.append(live_photo_video_id_item)

        local_offset_hours = self.local_offset_hours

        owner_id = self.owner_id

        projection_type = []
        for projection_type_item_data in self.projection_type:
            projection_type_item: Union[None, str]
            projection_type_item = projection_type_item_data
            projection_type.append(projection_type_item)

        ratio = self.ratio

        thumbhash = []
        for thumbhash_item_data in self.thumbhash:
            thumbhash_item: Union[None, str]
            thumbhash_item = thumbhash_item_data
            thumbhash.append(thumbhash_item)

        visibility = []
        for visibility_item_data in self.visibility:
            visibility_item = visibility_item_data.value
            visibility.append(visibility_item)

        latitude: Union[Unset, list[Union[None, float]]] = UNSET
        if not isinstance(self.latitude, Unset):
            latitude = []
            for latitude_item_data in self.latitude:
                latitude_item: Union[None, float]
                latitude_item = latitude_item_data
                latitude.append(latitude_item)

        longitude: Union[Unset, list[Union[None, float]]] = UNSET
        if not isinstance(self.longitude, Unset):
            longitude = []
            for longitude_item_data in self.longitude:
                longitude_item: Union[None, float]
                longitude_item = longitude_item_data
                longitude.append(longitude_item)

        stack: Union[Unset, list[Union[None, list[str]]]] = UNSET
        if not isinstance(self.stack, Unset):
            stack = []
            for stack_item_data in self.stack:
                stack_item: Union[None, list[str]]
                if isinstance(stack_item_data, list):
                    stack_item = stack_item_data

                else:
                    stack_item = stack_item_data
                stack.append(stack_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "city": city,
                "country": country,
                "duration": duration,
                "fileCreatedAt": file_created_at,
                "id": id,
                "isFavorite": is_favorite,
                "isImage": is_image,
                "isTrashed": is_trashed,
                "livePhotoVideoId": live_photo_video_id,
                "localOffsetHours": local_offset_hours,
                "ownerId": owner_id,
                "projectionType": projection_type,
                "ratio": ratio,
                "thumbhash": thumbhash,
                "visibility": visibility,
            }
        )
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if stack is not UNSET:
            field_dict["stack"] = stack

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        city = []
        _city = d.pop("city")
        for city_item_data in _city:

            def _parse_city_item(data: object) -> Union[None, str]:
                if data is None:
                    return data
                return cast(Union[None, str], data)

            city_item = _parse_city_item(city_item_data)

            city.append(city_item)

        country = []
        _country = d.pop("country")
        for country_item_data in _country:

            def _parse_country_item(data: object) -> Union[None, str]:
                if data is None:
                    return data
                return cast(Union[None, str], data)

            country_item = _parse_country_item(country_item_data)

            country.append(country_item)

        duration = []
        _duration = d.pop("duration")
        for duration_item_data in _duration:

            def _parse_duration_item(data: object) -> Union[None, str]:
                if data is None:
                    return data
                return cast(Union[None, str], data)

            duration_item = _parse_duration_item(duration_item_data)

            duration.append(duration_item)

        file_created_at = cast(list[str], d.pop("fileCreatedAt"))

        id = cast(list[str], d.pop("id"))

        is_favorite = cast(list[bool], d.pop("isFavorite"))

        is_image = cast(list[bool], d.pop("isImage"))

        is_trashed = cast(list[bool], d.pop("isTrashed"))

        live_photo_video_id = []
        _live_photo_video_id = d.pop("livePhotoVideoId")
        for live_photo_video_id_item_data in _live_photo_video_id:

            def _parse_live_photo_video_id_item(data: object) -> Union[None, str]:
                if data is None:
                    return data
                return cast(Union[None, str], data)

            live_photo_video_id_item = _parse_live_photo_video_id_item(
                live_photo_video_id_item_data
            )

            live_photo_video_id.append(live_photo_video_id_item)

        local_offset_hours = cast(list[float], d.pop("localOffsetHours"))

        owner_id = cast(list[str], d.pop("ownerId"))

        projection_type = []
        _projection_type = d.pop("projectionType")
        for projection_type_item_data in _projection_type:

            def _parse_projection_type_item(data: object) -> Union[None, str]:
                if data is None:
                    return data
                return cast(Union[None, str], data)

            projection_type_item = _parse_projection_type_item(
                projection_type_item_data
            )

            projection_type.append(projection_type_item)

        ratio = cast(list[float], d.pop("ratio"))

        thumbhash = []
        _thumbhash = d.pop("thumbhash")
        for thumbhash_item_data in _thumbhash:

            def _parse_thumbhash_item(data: object) -> Union[None, str]:
                if data is None:
                    return data
                return cast(Union[None, str], data)

            thumbhash_item = _parse_thumbhash_item(thumbhash_item_data)

            thumbhash.append(thumbhash_item)

        visibility = []
        _visibility = d.pop("visibility")
        for visibility_item_data in _visibility:
            visibility_item = AssetVisibility(visibility_item_data)

            visibility.append(visibility_item)

        latitude = []
        _latitude = d.pop("latitude", UNSET)
        for latitude_item_data in _latitude or []:

            def _parse_latitude_item(data: object) -> Union[None, float]:
                if data is None:
                    return data
                return cast(Union[None, float], data)

            latitude_item = _parse_latitude_item(latitude_item_data)

            latitude.append(latitude_item)

        longitude = []
        _longitude = d.pop("longitude", UNSET)
        for longitude_item_data in _longitude or []:

            def _parse_longitude_item(data: object) -> Union[None, float]:
                if data is None:
                    return data
                return cast(Union[None, float], data)

            longitude_item = _parse_longitude_item(longitude_item_data)

            longitude.append(longitude_item)

        stack = []
        _stack = d.pop("stack", UNSET)
        for stack_item_data in _stack or []:

            def _parse_stack_item(data: object) -> Union[None, list[str]]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    stack_item_type_0 = cast(list[str], data)

                    return stack_item_type_0
                except:  # noqa: E722
                    pass
                return cast(Union[None, list[str]], data)

            stack_item = _parse_stack_item(stack_item_data)

            stack.append(stack_item)

        time_bucket_asset_response_dto = cls(
            city=city,
            country=country,
            duration=duration,
            file_created_at=file_created_at,
            id=id,
            is_favorite=is_favorite,
            is_image=is_image,
            is_trashed=is_trashed,
            live_photo_video_id=live_photo_video_id,
            local_offset_hours=local_offset_hours,
            owner_id=owner_id,
            projection_type=projection_type,
            ratio=ratio,
            thumbhash=thumbhash,
            visibility=visibility,
            latitude=latitude,
            longitude=longitude,
            stack=stack,
        )

        time_bucket_asset_response_dto.additional_properties = d
        return time_bucket_asset_response_dto

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
