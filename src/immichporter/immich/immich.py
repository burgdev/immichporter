from immichporter.immich.client import AuthenticatedClient
from typing import Type
from immichporter.immich.client.api.albums import (
    get_all_albums,
    create_album,
    delete_album,
)
import time
import re
from immichporter.immich.client.api.search import search_assets
from immichporter.immich.client.api.users_admin import (
    search_users_admin,
    create_user_admin,
)
from immichporter.immich.client.models import (
    MetadataSearchDto,
    SearchResponseDto,
    UserResponseDto,
    UserAdminCreateDto,
    AlbumUserCreateDto,
    CreateAlbumDto,
    AlbumResponseDto,
    JobCreateDto,
    JobCommandDto,
    ManualJobName,
    JobName,
    JobCommand,
    JobStatusDto,
)
from immichporter.immich.client.api.jobs import (
    create_job,
    get_all_jobs_status,
    send_job_command,
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
        self._api_key = api_key
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
        self, limit: int | None = None, shared: bool | None = None
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
        if limit is not None and limit > 0:
            albums = albums[:limit]

        return albums

    def create_album(
        self,
        name: str,
        description: str | None = None,
        users: list[AlbumUserCreateDto] | None = None,
        assets: list[str] | None = None,
    ) -> AlbumResponseDto:
        description = UNSET if description is None else description
        users = UNSET if users is None else users
        assets = UNSET if assets is None else assets
        body = CreateAlbumDto(
            album_name=name,
            description=description,
            album_users=users,
            asset_ids=assets,
        )
        response = create_album.sync_detailed(client=self.client, body=body)
        if response.status_code != 201:
            raise Exception(
                f"Failed to create album {response.status_code}: {response.content}"
            )
        return response.parsed

    def delete_album(
        self, album_id: str | None = None, album_name: str | None = None
    ) -> None:
        if album_id is None and album_name is None:
            raise ValueError("Either album_id or album_name must be provided")
        if album_id is None:
            albums = self.get_albums()
            for album in albums:
                if album.album_name == album_name:
                    album_id = album.id
                    break
        if album_id is None:
            raise ValueError(f"Album '{album_name}' not found")
        response = delete_album.sync_detailed(client=self.client, id=album_id)
        if response.status_code != 204:
            raise Exception(
                f"Failed to delete album {response.status_code}: {response.content}"
            )

    def search_assets(
        self,
        filename: str | None | Unset = None,
        taken: datetime | str | None | Unset = None,
        taken_before: datetime | str | None | Unset = None,
        taken_after: datetime | str | None | Unset = None,
        **options: any,
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

    def get_users(self, width_deleted: bool = True) -> list[UserResponseDto]:
        response = search_users_admin.sync_detailed(client=self.client)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch users: {response.content}")
        return response.parsed

    def add_user(
        self, name: str, email: str, password: str, quota_gb: int = 10
    ) -> UserResponseDto:
        quota_bytes = 1073741824 * quota_gb
        body = UserAdminCreateDto(
            name=name,
            email=email,
            password=password,
            notify=False,
            should_change_password=True,
            quota_size_in_bytes=quota_bytes,
        )
        response = create_user_admin.sync_detailed(client=self.client, body=body)
        if response.status_code != 201:
            raise Exception(
                f"Failed to create user {response.status_code}: {response.content}"
            )
        return response.parsed

    def start_job(self, job_name: ManualJobName | JobName) -> dict:
        """Start a new job with the given name.

        Args:
            job_name: Name of the job to start (must be a valid ManualJobName or JobName value)

        Returns:
            dict: The job status with keys: id, name, isActive, lastRun, nextRun

        Raises:
            Exception: If the job fails to start or status cannot be retrieved
        """
        try:
            # Create the job data
            if isinstance(job_name, ManualJobName):
                job_data = JobCreateDto(name=ManualJobName(job_name))

                # Send the request to create the job
                response = create_job.sync_detailed(client=self._client, body=job_data)

                # 204 No Content is expected on success
                if response.status_code != 204:
                    raise Exception(
                        f"Failed to start job {job_name}: {response.content}"
                    )
                return True
            elif isinstance(job_name, JobName):
                job_data = JobCreateDto(name=JobName(job_name))
                # Send the request to create the job
                body = JobCommandDto(command=JobCommand.START)
                response = send_job_command.sync_detailed(
                    id=job_name, client=self._client, body=body
                )
                if response.status_code == 400:
                    if (
                        "job is already running"
                        in response.content.decode("utf-8").lower()
                    ):
                        console.print(
                            f"Job [blue]'{job_name}'[/] is already running, maybe you need to restart it later manually!"
                        )
                        return True

                if not response.status_code.is_success:
                    raise Exception(
                        f"Failed to start job {job_name} (status code: {response.status_code}): {response.content}"
                    )
                job_status = response.parsed
                return job_status.job_counts.active >= 0

        except Exception as e:
            raise Exception(f"Error starting job {job_name}: {str(e)}") from e

    def get_job_status(self, job_name: JobName) -> JobStatusDto:
        """Get the status of a job by name.

        Args:
            job_name: Name of the job to check

        Returns:
            dict: The job status with keys: id, name, isActive, lastRun, nextRun

        Raises:
            Exception: If the job status cannot be retrieved
        """
        try:
            response = get_all_jobs_status.sync_detailed(client=self._client)
            if not response.status_code.is_success:
                raise Exception(
                    f"Failed to get job status (status code: {response.status_code}): {response.content}"
                )

            resp_parsed = response.parsed
            job_name_snake = re.sub(r"([a-z])([A-Z])", r"\1_\2", job_name).lower()
            job_status = getattr(resp_parsed, job_name_snake, None)
            if not job_status:
                raise Exception(f"Could not find status for job {job_name}")

            return job_status

        except Exception as e:
            raise Exception(f"Error getting job status for {job_name}: {str(e)}")

    def run_db_backup(self, wait_time_s: int = 15):
        self.start_job(ManualJobName.BACKUP_DATABASE)
        time.sleep(wait_time_s)


if __name__ == "__main__":
    import os

    endpoint = os.getenv("IMMICH_ENDPOINT")
    api_key = os.getenv("IMMICH_API_KEY")
    insecure = os.getenv("IMMICH_INSECURE") == "1"
    client = ImmichClient(endpoint=endpoint, api_key=api_key, insecure=insecure)
    console.print(f"Endpoint: {client.endpoint}")
    console.print(f"API Key: [yellow]'{client._api_key}'[/]")
    # albums = client.search_assets(
    #   filename="20250113_101105.jpg", taken=None
    # )
    # console.print(albums)
    # users = client.get_users()
    # console.print(users)
    # album = client.create_album("Test Album")
    # console.print(album)
    client.delete_album(album_name="Ralligstöck, 22.8.25")
    albums = client.get_albums()
    console.print([a.album_name for a in albums])
