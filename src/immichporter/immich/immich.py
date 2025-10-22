from immichporter.immich.client.models.bulk_ids_dto import BulkIdsDto
from immichporter.immich.client.models.asset_response_dto import AssetResponseDto
from immichporter.immich.client import AuthenticatedClient
from typing import Type, Any
from immichporter.immich.client.api.albums import (
    get_all_albums,
    create_album,
    delete_album,
)
import time
import re
from immichporter.immich.client.api.timeline import get_time_bucket, get_time_buckets
from immichporter.immich.client.api.tags import (
    get_all_tags,
    untag_assets,
    delete_tag,
    get_tag_by_id,
)
from immichporter.immich.client.api.search import search_assets
from immichporter.immich.client.api.users_admin import (
    search_users_admin,
    create_user_admin,
)
from uuid import UUID
from immichporter.immich.client.models import (
    TagResponseDto,
    MetadataSearchDto,
    UserAdminCreateDto,
    AlbumUserCreateDto,
    CreateAlbumDto,
    AlbumResponseDto,
    JobCreateDto,
    UserAdminResponseDto,
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
from loguru import logger

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
        base_url=base_url,  # type: ignore
        token=api_key,
        auth_header_name="x-api-key",
        prefix="",
        verify_ssl=not insecure,  # type: ignore
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
        if client is not None:
            self._client = client
        else:
            assert (
                endpoint is not None
            ), "'endpoint' must be provided if 'client' is not provided"
            assert (
                api_key is not None
            ), "'api_key' must be provided if 'client' is not provided"
            self._client = immich_api_client(
                endpoint=endpoint, api_key=api_key, insecure=insecure
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
        shared: Unset | bool = UNSET if shared is None else shared
        response = get_all_albums.sync_detailed(client=self.client, shared=shared)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch albums: {response.content}")

        assert response.parsed is not None
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
        description: Unset | str = UNSET if description is None else description
        users: Unset | list[AlbumUserCreateDto] = UNSET if users is None else users
        assets: Unset | list[UUID] = (
            UNSET if assets is None else [UUID(a) for a in assets]
        )
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
        assert response.parsed is not None
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
        response = delete_album.sync_detailed(client=self.client, id=UUID(album_id))
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
        **options: dict[str, Any],
    ) -> list[AssetResponseDto]:
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
            **options,  # type: ignore
        )
        response = search_assets.sync_detailed(client=self.client, body=search_dto)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch albums: {response.content}")

        assets = response.parsed
        assert assets is not None

        return assets.assets.items

    def get_users(self, width_deleted: bool = True) -> list[UserAdminResponseDto]:
        response = search_users_admin.sync_detailed(client=self.client)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch users: {response.content}")
        assert response.parsed is not None
        return response.parsed

    def add_user(
        self, name: str, email: str, password: str, quota_gb: int = 10
    ) -> UserAdminResponseDto:
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
        res = response.parsed
        assert res is not None
        return res

    def start_job(self, job_name: ManualJobName | JobName) -> bool:
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

                if not response.status_code.is_success:  # type: ignore
                    raise Exception(
                        f"Failed to start job {job_name} (status code: {response.status_code}): {response.content}"
                    )
                job_status = response.parsed
                assert job_status is not None
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
            if not response.status_code.is_success:  # type: ignore
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

    def get_tags(
        self,
        filter_name: str | None = None,
        filter_value: str | None = None,
        parent_id: UUID | str | None = None,
    ) -> list[TagResponseDto]:
        """Get all tags from Immich.

        Args:
            filter_name (str | None, optional): Filter tags by name (e.g. `TagName`). Defaults to None.
            filter_value (str | None, optional): Filter tags by value (parents included, e.g. `Parent/TagName`). Defaults to None.
            parent_id (UUID | str | None, optional): Filter tags by parent ID (either UUID or name, e.g. `Parent`). Defaults to None.

        Returns:
            List of tags
        """
        response = get_all_tags.sync_detailed(client=self._client)
        if not response.status_code.is_success:  # type: ignore
            raise Exception(
                f"Failed to get tags (status code: {response.status_code}): {response.content}"
            )
        tags = response.parsed
        if not tags:
            raise Exception("Could not find tags")
        if parent_id:
            if isinstance(parent_id, UUID):
                parent_uuid = str(parent_id)
            else:
                try:
                    parent_uuid = UUID(parent_id)
                except ValueError:
                    parent_tags = self.get_tags(filter=parent_id)
                    if not parent_tags:
                        raise Exception(f"Could not find tag with name {parent_id}")
                    parent_uuid = parent_tags[0].id
            tags = [tag for tag in tags if tag.parent_id == str(parent_uuid)]
        if filter_value:
            tags = [tag for tag in tags if filter_value in tag.value]
        if filter_name:
            tags = [tag for tag in tags if filter_name in tag.name]
        return tags

    def timeline_assets(self, tag_id: UUID | str | None = None, **kwargs):
        """Get all assets from Immich by tag ID or **kwargs."""
        tag_id_arg = (
            tag_id if isinstance(tag_id, UUID) else UUID(tag_id) if tag_id else UNSET
        )
        response = get_time_buckets.sync_detailed(
            client=self._client, tag_id=tag_id_arg, **kwargs
        )
        if not response.status_code.is_success:  # type: ignore
            raise Exception(
                f"Failed to get time buckets (status code: {response.status_code}): {response.content}"
            )
        time_buckets = response.parsed
        if time_buckets is None:
            raise Exception("Could not find time buckets")
        for time_bucket in time_buckets:
            time_bucket_ts = time_bucket.time_bucket
            resp = get_time_bucket.sync_detailed(
                client=self._client,
                tag_id=tag_id_arg,
                time_bucket=time_bucket_ts,
                **kwargs,
            )
            if not resp.status_code.is_success:  # type: ignore
                raise Exception(
                    f"Failed to get time bucket (status code: {resp.status_code}): {resp.content}"
                )
            resp_parsed = resp.parsed
            if not resp_parsed:
                raise Exception("Could not find time bucket")
            for asset_id in resp_parsed.id:
                yield asset_id

    def untag_assets(
        self,
        tag: TagResponseDto | str | UUID,
        asset_ids: list[UUID | str] | None = None,
        remove_tag: bool = False,
    ) -> int:
        if isinstance(tag, str):
            tag = self.get_tags(filter_name=tag)[0].id
        elif isinstance(tag, UUID):
            res = get_tag_by_id.sync(client=self._client, id=tag)
            if res is None:
                raise Exception(f"Could not find tag with id {tag}")
            tag = res
        if isinstance(tag, TagResponseDto):
            tag_id = tag.id
        else:
            raise Exception(f"Invalid tag type: {type(tag)}")

        removed = 0
        # check if there are children:
        children = self.get_tags(parent_id=tag_id)
        if children:
            logger.info(f"Tag {tag_id} has children, removing them first")
            # we need to remove children first:
            for child in children:
                removed += self.untag_assets(tag=child, remove_tag=remove_tag)

        if asset_ids is None:
            asset_ids = list(self.timeline_assets(tag_id=tag_id))
        asset_ids = [
            UUID(asset_id) if isinstance(asset_id, str) else asset_id
            for asset_id in asset_ids
        ]
        logger.debug(
            f"Untagging {len(asset_ids)} assets with tag '{tag.value}' ({tag_id})"
        )
        tag_id = UUID(tag_id) if isinstance(tag_id, str) else tag_id
        body = BulkIdsDto(ids=asset_ids)
        response = untag_assets.sync_detailed(client=self._client, id=tag_id, body=body)
        if not response.status_code.is_success:  # type: ignore
            raise Exception(
                f"Failed to untag assets (status code: {response.status_code}): {response.content}"
            )
        removed += len(asset_ids)
        if remove_tag:
            logger.debug(f"Removing tag '{tag.value}' ({tag_id})")
            response = delete_tag.sync_detailed(client=self._client, id=tag_id)
            if not response.status_code.is_success:  # type: ignore
                raise Exception(
                    f"Failed to delete tag (status code: {response.status_code}): {response.content}"
                )
        return removed


if __name__ == "__main__":
    import os

    endpoint = os.getenv("IMMICH_ENDPOINT")
    api_key = os.getenv("IMMICH_API_KEY")
    insecure = os.getenv("IMMICH_INSECURE") == "1"
    client = ImmichClient(endpoint=endpoint, api_key=api_key, insecure=insecure)
    console.print(f"Endpoint: {client.endpoint}")
    console.print(f"API Key: [yellow]'{client._api_key}'[/]")
    tag_filter = "from_google"
    tag_filter = None
    # tag_parent_id = UUID("a94b0135-727d-4f32-9b43-c99d5ac7d92e")
    # tag_parent_id = "People"
    tag_parent_id = None
    tags = client.get_tags(filter_name=tag_filter, parent_id=tag_parent_id)
    for tag in tags:
        console.print(tag.value)
    # tag = tags[0]
    ##console.print(tags)
    # console.print(tag)
    # removed = client.untag_assets(tag=tag, remove_tag=True)
    # console.print(f"Removed {removed} assets")
    ##for asset_id in client.search_assets(tag_id=tag.id):
    #    #console.print(asset_id)
