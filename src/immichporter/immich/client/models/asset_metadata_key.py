from enum import Enum


class AssetMetadataKey(str, Enum):
    MOBILE_APP = "mobile-app"

    def __str__(self) -> str:
        return str(self.value)
