from enum import Enum


class AssetVisibility(str, Enum):
    ARCHIVE = "archive"
    HIDDEN = "hidden"
    LOCKED = "locked"
    TIMELINE = "timeline"

    def __str__(self) -> str:
        return str(self.value)
