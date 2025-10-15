from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SystemConfigNightlyTasksDto")


@_attrs_define
class SystemConfigNightlyTasksDto:
    """
    Attributes:
        cluster_new_faces (bool):
        database_cleanup (bool):
        generate_memories (bool):
        missing_thumbnails (bool):
        start_time (str):
        sync_quota_usage (bool):
    """

    cluster_new_faces: bool
    database_cleanup: bool
    generate_memories: bool
    missing_thumbnails: bool
    start_time: str
    sync_quota_usage: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cluster_new_faces = self.cluster_new_faces

        database_cleanup = self.database_cleanup

        generate_memories = self.generate_memories

        missing_thumbnails = self.missing_thumbnails

        start_time = self.start_time

        sync_quota_usage = self.sync_quota_usage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "clusterNewFaces": cluster_new_faces,
                "databaseCleanup": database_cleanup,
                "generateMemories": generate_memories,
                "missingThumbnails": missing_thumbnails,
                "startTime": start_time,
                "syncQuotaUsage": sync_quota_usage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cluster_new_faces = d.pop("clusterNewFaces")

        database_cleanup = d.pop("databaseCleanup")

        generate_memories = d.pop("generateMemories")

        missing_thumbnails = d.pop("missingThumbnails")

        start_time = d.pop("startTime")

        sync_quota_usage = d.pop("syncQuotaUsage")

        system_config_nightly_tasks_dto = cls(
            cluster_new_faces=cluster_new_faces,
            database_cleanup=database_cleanup,
            generate_memories=generate_memories,
            missing_thumbnails=missing_thumbnails,
            start_time=start_time,
            sync_quota_usage=sync_quota_usage,
        )

        system_config_nightly_tasks_dto.additional_properties = d
        return system_config_nightly_tasks_dto

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
