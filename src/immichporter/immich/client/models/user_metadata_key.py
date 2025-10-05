from enum import Enum


class UserMetadataKey(str, Enum):
    LICENSE = "license"
    ONBOARDING = "onboarding"
    PREFERENCES = "preferences"

    def __str__(self) -> str:
        return str(self.value)
