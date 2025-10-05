from enum import Enum


class OAuthTokenEndpointAuthMethod(str, Enum):
    CLIENT_SECRET_BASIC = "client_secret_basic"
    CLIENT_SECRET_POST = "client_secret_post"

    def __str__(self) -> str:
        return str(self.value)
