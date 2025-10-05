from enum import Enum


class AssetMediaSize(str, Enum):
    FULLSIZE = "fullsize"
    PREVIEW = "preview"
    THUMBNAIL = "thumbnail"

    def __str__(self) -> str:
        return str(self.value)
