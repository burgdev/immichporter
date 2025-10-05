from enum import Enum


class ManualJobName(str, Enum):
    BACKUP_DATABASE = "backup-database"
    MEMORY_CLEANUP = "memory-cleanup"
    MEMORY_CREATE = "memory-create"
    PERSON_CLEANUP = "person-cleanup"
    TAG_CLEANUP = "tag-cleanup"
    USER_CLEANUP = "user-cleanup"

    def __str__(self) -> str:
        return str(self.value)
