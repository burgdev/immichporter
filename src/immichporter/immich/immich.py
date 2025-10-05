from immichporter.immich.client import AuthenticatedClient
from typing import Type
from immichporter.immich.client.api.albums import get_all_albums
from immichporter.immich.client.api.search import search_assets
from immichporter.immich.client.models import (
    AlbumResponseDto,
    MetadataSearchDto,
    SearchResponseDto,
)
from immichporter.immich.client.types import UNSET, Unset
from rich.console import Console
from datetime import datetime, timedelta

console = Console()
ImmichApiClient: Type[AuthenticatedClient] = AuthenticatedClient


def immich_api_client(
    endpoint: str, api_key: str, insecure: bool = False
) -> ImmichApiClient:
    """Returns immich api client"""
    base_url = endpoint.rstrip("/")
    if not base_url.endswith("/api"):
        base_url = f"{base_url}/api"
    client = AuthenticatedClient(
        base_url=base_url,
        token=api_key,
        auth_header_name="x-api-key",
        prefix="",
        verify_ssl=not insecure,
    )

    return client


class ImmichClient:
    def __init__(
        self,
        client: ImmichApiClient | None = None,
        endpoint: str | None = None,
        api_key: str | None = None,
        insecure: bool = False,
    ):
        """Immich client with specific functions, often an API wrapper."""
        self._client = (
            client
            if client is not None
            else immich_api_client(
                endpoint=endpoint, api_key=api_key, insecure=insecure
            )
        )

    @property
    def client(self) -> ImmichApiClient:
        return self._client

    @property
    def endpoint(self) -> str:
        """Returns the base url of the Immich server"""
        return self.client._base_url

    def get_albums(
        self, limit: int = 50, shared: bool | None = None
    ) -> list[AlbumResponseDto]:
        """List all albums on the Immich server.

        Args:
            limit: Maximum number of albums to return
            shared: Filter by shared status (True for shared, False for not shared, None for all)
        """
        response = get_all_albums.sync_detailed(client=self.client, shared=shared)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch albums: {response.content}")

        albums: list[AlbumResponseDto] = response.parsed

        # Sort albums by name
        albums = sorted(albums, key=lambda x: x.album_name.lower())

        # Apply limit
        if limit > 0:
            albums = albums[:limit]

        return albums

    def search_assets(
        self,
        filename: str | None | Unset = None,
        taken: datetime | str | None | Unset = None,
        taken_before: datetime | str | None | Unset = None,
        taken_after: datetime | str | None | Unset = None,
        **options,
    ) -> list[AlbumResponseDto]:
        """Search for assets on the Immich server.

        Dates can be formate as follow:
        Python `datetime` or string with the format `%Y-%m-%d %H:%M:%S` or `%Y-%m-%d`

        Args:
            filename: Filter by filename
            taken: Filter by taken date (plus minus 1 day if no time is given, resp. minus 2 hours if no day is given)
            taken_before: Filter by taken date before, cannot be used together with `taken`.
            taken_after: Filter by taken date after, cannot be used together with `taken`.
            **options: Additional options, see https://api.immich.app/endpoints/search/searchAssets for more information
        """
        filename = UNSET if filename is None else filename
        taken_before = UNSET if taken_before is None else taken_before
        taken_after = UNSET if taken_after is None else taken_after
        if isinstance(taken_before, str):
            if " " not in taken_before:
                taken_before += " 00:00:00"
            taken_before = datetime.strptime(taken_before, "%Y-%m-%d %H:%M:%S")
        if isinstance(taken_after, str):
            if " " not in taken_after:
                taken_after += " 00:00:00"
            taken_after = datetime.strptime(taken_after, "%Y-%m-%d %H:%M:%S")
        if taken:
            assert (
                taken_before is UNSET and taken_after is UNSET
            ), "'taken_before' and 'taken_after' must be unset if 'taken' is set"
            delta_before = timedelta(hours=2)
            delta_after = timedelta(hours=2)
            if isinstance(taken, str):
                if " " not in taken:
                    taken += " 00:00:00"
                    delta_before = timedelta(days=1)
                    delta_after = timedelta(days=0)
                taken = datetime.strptime(taken, "%Y-%m-%d %H:%M:%S")
            taken_before = taken + delta_before
            taken_after = taken - delta_after

        search_dto = MetadataSearchDto(
            original_file_name=filename,
            taken_before=taken_before,
            taken_after=taken_after,
            **options,
        )
        response = search_assets.sync_detailed(client=self.client, body=search_dto)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch albums: {response.content}")

        assets: list[SearchResponseDto] = response.parsed

        return assets.assets.items


if __name__ == "__main__":
    import os

    endpoint = os.getenv("IMMICH_ENDPOINT")
    api_key = os.getenv("IMMICH_API_KEY")
    insecure = os.getenv("IMMICH_INSECURE") == "1"
    client = ImmichClient(endpoint=endpoint, api_key=api_key, insecure=insecure)
    albums = client.search_assets(
        filename="20250830_114716.jpg", taken="2025-08-30 09:50:00"
    )
    console.print(albums)
