from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.clip_config import CLIPConfig
    from ..models.duplicate_detection_config import DuplicateDetectionConfig
    from ..models.facial_recognition_config import FacialRecognitionConfig
    from ..models.machine_learning_availability_checks_dto import (
        MachineLearningAvailabilityChecksDto,
    )


T = TypeVar("T", bound="SystemConfigMachineLearningDto")


@_attrs_define
class SystemConfigMachineLearningDto:
    """
    Attributes:
        availability_checks (MachineLearningAvailabilityChecksDto):
        clip (CLIPConfig):
        duplicate_detection (DuplicateDetectionConfig):
        enabled (bool):
        facial_recognition (FacialRecognitionConfig):
        urls (list[str]):
    """

    availability_checks: "MachineLearningAvailabilityChecksDto"
    clip: "CLIPConfig"
    duplicate_detection: "DuplicateDetectionConfig"
    enabled: bool
    facial_recognition: "FacialRecognitionConfig"
    urls: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        availability_checks = self.availability_checks.to_dict()

        clip = self.clip.to_dict()

        duplicate_detection = self.duplicate_detection.to_dict()

        enabled = self.enabled

        facial_recognition = self.facial_recognition.to_dict()

        urls = self.urls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "availabilityChecks": availability_checks,
                "clip": clip,
                "duplicateDetection": duplicate_detection,
                "enabled": enabled,
                "facialRecognition": facial_recognition,
                "urls": urls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.clip_config import CLIPConfig
        from ..models.duplicate_detection_config import DuplicateDetectionConfig
        from ..models.facial_recognition_config import FacialRecognitionConfig
        from ..models.machine_learning_availability_checks_dto import (
            MachineLearningAvailabilityChecksDto,
        )

        d = dict(src_dict)
        availability_checks = MachineLearningAvailabilityChecksDto.from_dict(
            d.pop("availabilityChecks")
        )

        clip = CLIPConfig.from_dict(d.pop("clip"))

        duplicate_detection = DuplicateDetectionConfig.from_dict(
            d.pop("duplicateDetection")
        )

        enabled = d.pop("enabled")

        facial_recognition = FacialRecognitionConfig.from_dict(
            d.pop("facialRecognition")
        )

        urls = cast(list[str], d.pop("urls"))

        system_config_machine_learning_dto = cls(
            availability_checks=availability_checks,
            clip=clip,
            duplicate_detection=duplicate_detection,
            enabled=enabled,
            facial_recognition=facial_recognition,
            urls=urls,
        )

        system_config_machine_learning_dto.additional_properties = d
        return system_config_machine_learning_dto

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
