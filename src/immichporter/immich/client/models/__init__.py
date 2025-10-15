"""Contains all the data models used in inputs/outputs"""

from .activity_create_dto import ActivityCreateDto
from .activity_response_dto import ActivityResponseDto
from .activity_statistics_response_dto import ActivityStatisticsResponseDto
from .add_users_dto import AddUsersDto
from .admin_onboarding_update_dto import AdminOnboardingUpdateDto
from .album_response_dto import AlbumResponseDto
from .album_statistics_response_dto import AlbumStatisticsResponseDto
from .album_user_add_dto import AlbumUserAddDto
from .album_user_create_dto import AlbumUserCreateDto
from .album_user_response_dto import AlbumUserResponseDto
from .album_user_role import AlbumUserRole
from .albums_add_assets_dto import AlbumsAddAssetsDto
from .albums_add_assets_response_dto import AlbumsAddAssetsResponseDto
from .albums_response import AlbumsResponse
from .albums_update import AlbumsUpdate
from .all_job_status_response_dto import AllJobStatusResponseDto
from .api_key_create_dto import APIKeyCreateDto
from .api_key_create_response_dto import APIKeyCreateResponseDto
from .api_key_response_dto import APIKeyResponseDto
from .api_key_update_dto import APIKeyUpdateDto
from .asset_bulk_delete_dto import AssetBulkDeleteDto
from .asset_bulk_update_dto import AssetBulkUpdateDto
from .asset_bulk_upload_check_dto import AssetBulkUploadCheckDto
from .asset_bulk_upload_check_item import AssetBulkUploadCheckItem
from .asset_bulk_upload_check_response_dto import AssetBulkUploadCheckResponseDto
from .asset_bulk_upload_check_result import AssetBulkUploadCheckResult
from .asset_bulk_upload_check_result_action import AssetBulkUploadCheckResultAction
from .asset_bulk_upload_check_result_reason import AssetBulkUploadCheckResultReason
from .asset_delta_sync_dto import AssetDeltaSyncDto
from .asset_delta_sync_response_dto import AssetDeltaSyncResponseDto
from .asset_face_create_dto import AssetFaceCreateDto
from .asset_face_delete_dto import AssetFaceDeleteDto
from .asset_face_response_dto import AssetFaceResponseDto
from .asset_face_update_dto import AssetFaceUpdateDto
from .asset_face_update_item import AssetFaceUpdateItem
from .asset_face_without_person_response_dto import AssetFaceWithoutPersonResponseDto
from .asset_full_sync_dto import AssetFullSyncDto
from .asset_ids_dto import AssetIdsDto
from .asset_ids_response_dto import AssetIdsResponseDto
from .asset_ids_response_dto_error import AssetIdsResponseDtoError
from .asset_job_name import AssetJobName
from .asset_jobs_dto import AssetJobsDto
from .asset_media_create_dto import AssetMediaCreateDto
from .asset_media_replace_dto import AssetMediaReplaceDto
from .asset_media_response_dto import AssetMediaResponseDto
from .asset_media_size import AssetMediaSize
from .asset_media_status import AssetMediaStatus
from .asset_metadata_key import AssetMetadataKey
from .asset_metadata_response_dto import AssetMetadataResponseDto
from .asset_metadata_response_dto_value import AssetMetadataResponseDtoValue
from .asset_metadata_upsert_dto import AssetMetadataUpsertDto
from .asset_metadata_upsert_item_dto import AssetMetadataUpsertItemDto
from .asset_metadata_upsert_item_dto_value import AssetMetadataUpsertItemDtoValue
from .asset_order import AssetOrder
from .asset_response_dto import AssetResponseDto
from .asset_stack_response_dto import AssetStackResponseDto
from .asset_stats_response_dto import AssetStatsResponseDto
from .asset_type_enum import AssetTypeEnum
from .asset_visibility import AssetVisibility
from .audio_codec import AudioCodec
from .auth_status_response_dto import AuthStatusResponseDto
from .avatar_update import AvatarUpdate
from .bulk_id_error_reason import BulkIdErrorReason
from .bulk_id_response_dto import BulkIdResponseDto
from .bulk_id_response_dto_error import BulkIdResponseDtoError
from .bulk_ids_dto import BulkIdsDto
from .cast_response import CastResponse
from .cast_update import CastUpdate
from .change_password_dto import ChangePasswordDto
from .check_existing_assets_dto import CheckExistingAssetsDto
from .check_existing_assets_response_dto import CheckExistingAssetsResponseDto
from .clip_config import CLIPConfig
from .colorspace import Colorspace
from .cq_mode import CQMode
from .create_album_dto import CreateAlbumDto
from .create_library_dto import CreateLibraryDto
from .create_profile_image_dto import CreateProfileImageDto
from .create_profile_image_response_dto import CreateProfileImageResponseDto
from .database_backup_config import DatabaseBackupConfig
from .download_archive_info import DownloadArchiveInfo
from .download_info_dto import DownloadInfoDto
from .download_response import DownloadResponse
from .download_response_dto import DownloadResponseDto
from .download_update import DownloadUpdate
from .duplicate_detection_config import DuplicateDetectionConfig
from .duplicate_response_dto import DuplicateResponseDto
from .email_notifications_response import EmailNotificationsResponse
from .email_notifications_update import EmailNotificationsUpdate
from .exif_response_dto import ExifResponseDto
from .face_dto import FaceDto
from .facial_recognition_config import FacialRecognitionConfig
from .folders_response import FoldersResponse
from .folders_update import FoldersUpdate
from .image_format import ImageFormat
from .job_command import JobCommand
from .job_command_dto import JobCommandDto
from .job_counts_dto import JobCountsDto
from .job_create_dto import JobCreateDto
from .job_name import JobName
from .job_settings_dto import JobSettingsDto
from .job_status_dto import JobStatusDto
from .library_response_dto import LibraryResponseDto
from .library_stats_response_dto import LibraryStatsResponseDto
from .license_key_dto import LicenseKeyDto
from .license_response_dto import LicenseResponseDto
from .log_level import LogLevel
from .login_credential_dto import LoginCredentialDto
from .login_response_dto import LoginResponseDto
from .logout_response_dto import LogoutResponseDto
from .machine_learning_availability_checks_dto import (
    MachineLearningAvailabilityChecksDto,
)
from .manual_job_name import ManualJobName
from .map_marker_response_dto import MapMarkerResponseDto
from .map_reverse_geocode_response_dto import MapReverseGeocodeResponseDto
from .memories_response import MemoriesResponse
from .memories_update import MemoriesUpdate
from .memory_create_dto import MemoryCreateDto
from .memory_response_dto import MemoryResponseDto
from .memory_statistics_response_dto import MemoryStatisticsResponseDto
from .memory_type import MemoryType
from .memory_update_dto import MemoryUpdateDto
from .merge_person_dto import MergePersonDto
from .metadata_search_dto import MetadataSearchDto
from .notification_create_dto import NotificationCreateDto
from .notification_create_dto_data import NotificationCreateDtoData
from .notification_delete_all_dto import NotificationDeleteAllDto
from .notification_dto import NotificationDto
from .notification_dto_data import NotificationDtoData
from .notification_level import NotificationLevel
from .notification_type import NotificationType
from .notification_update_all_dto import NotificationUpdateAllDto
from .notification_update_dto import NotificationUpdateDto
from .o_auth_authorize_response_dto import OAuthAuthorizeResponseDto
from .o_auth_callback_dto import OAuthCallbackDto
from .o_auth_config_dto import OAuthConfigDto
from .o_auth_token_endpoint_auth_method import OAuthTokenEndpointAuthMethod
from .on_this_day_dto import OnThisDayDto
from .onboarding_dto import OnboardingDto
from .onboarding_response_dto import OnboardingResponseDto
from .partner_create_dto import PartnerCreateDto
from .partner_direction import PartnerDirection
from .partner_response_dto import PartnerResponseDto
from .partner_update_dto import PartnerUpdateDto
from .people_response import PeopleResponse
from .people_response_dto import PeopleResponseDto
from .people_update import PeopleUpdate
from .people_update_dto import PeopleUpdateDto
from .people_update_item import PeopleUpdateItem
from .permission import Permission
from .person_create_dto import PersonCreateDto
from .person_response_dto import PersonResponseDto
from .person_statistics_response_dto import PersonStatisticsResponseDto
from .person_update_dto import PersonUpdateDto
from .person_with_faces_response_dto import PersonWithFacesResponseDto
from .pin_code_change_dto import PinCodeChangeDto
from .pin_code_reset_dto import PinCodeResetDto
from .pin_code_setup_dto import PinCodeSetupDto
from .places_response_dto import PlacesResponseDto
from .purchase_response import PurchaseResponse
from .purchase_update import PurchaseUpdate
from .queue_status_dto import QueueStatusDto
from .random_search_dto import RandomSearchDto
from .ratings_response import RatingsResponse
from .ratings_update import RatingsUpdate
from .reaction_level import ReactionLevel
from .reaction_type import ReactionType
from .reverse_geocoding_state_response_dto import ReverseGeocodingStateResponseDto
from .search_album_response_dto import SearchAlbumResponseDto
from .search_asset_response_dto import SearchAssetResponseDto
from .search_explore_item import SearchExploreItem
from .search_explore_response_dto import SearchExploreResponseDto
from .search_facet_count_response_dto import SearchFacetCountResponseDto
from .search_facet_response_dto import SearchFacetResponseDto
from .search_response_dto import SearchResponseDto
from .search_statistics_response_dto import SearchStatisticsResponseDto
from .search_suggestion_type import SearchSuggestionType
from .server_about_response_dto import ServerAboutResponseDto
from .server_apk_links_dto import ServerApkLinksDto
from .server_config_dto import ServerConfigDto
from .server_features_dto import ServerFeaturesDto
from .server_media_types_response_dto import ServerMediaTypesResponseDto
from .server_ping_response import ServerPingResponse
from .server_stats_response_dto import ServerStatsResponseDto
from .server_storage_response_dto import ServerStorageResponseDto
from .server_theme_dto import ServerThemeDto
from .server_version_history_response_dto import ServerVersionHistoryResponseDto
from .server_version_response_dto import ServerVersionResponseDto
from .session_create_dto import SessionCreateDto
from .session_create_response_dto import SessionCreateResponseDto
from .session_response_dto import SessionResponseDto
from .session_unlock_dto import SessionUnlockDto
from .session_update_dto import SessionUpdateDto
from .shared_link_create_dto import SharedLinkCreateDto
from .shared_link_edit_dto import SharedLinkEditDto
from .shared_link_response_dto import SharedLinkResponseDto
from .shared_link_type import SharedLinkType
from .shared_links_response import SharedLinksResponse
from .shared_links_update import SharedLinksUpdate
from .sign_up_dto import SignUpDto
from .smart_search_dto import SmartSearchDto
from .source_type import SourceType
from .stack_create_dto import StackCreateDto
from .stack_response_dto import StackResponseDto
from .stack_update_dto import StackUpdateDto
from .statistics_search_dto import StatisticsSearchDto
from .sync_ack_delete_dto import SyncAckDeleteDto
from .sync_ack_dto import SyncAckDto
from .sync_ack_set_dto import SyncAckSetDto
from .sync_ack_v1 import SyncAckV1
from .sync_album_delete_v1 import SyncAlbumDeleteV1
from .sync_album_to_asset_delete_v1 import SyncAlbumToAssetDeleteV1
from .sync_album_to_asset_v1 import SyncAlbumToAssetV1
from .sync_album_user_delete_v1 import SyncAlbumUserDeleteV1
from .sync_album_user_v1 import SyncAlbumUserV1
from .sync_album_v1 import SyncAlbumV1
from .sync_asset_delete_v1 import SyncAssetDeleteV1
from .sync_asset_exif_v1 import SyncAssetExifV1
from .sync_asset_face_delete_v1 import SyncAssetFaceDeleteV1
from .sync_asset_face_v1 import SyncAssetFaceV1
from .sync_asset_metadata_delete_v1 import SyncAssetMetadataDeleteV1
from .sync_asset_metadata_v1 import SyncAssetMetadataV1
from .sync_asset_metadata_v1_value import SyncAssetMetadataV1Value
from .sync_asset_v1 import SyncAssetV1
from .sync_auth_user_v1 import SyncAuthUserV1
from .sync_complete_v1 import SyncCompleteV1
from .sync_entity_type import SyncEntityType
from .sync_memory_asset_delete_v1 import SyncMemoryAssetDeleteV1
from .sync_memory_asset_v1 import SyncMemoryAssetV1
from .sync_memory_delete_v1 import SyncMemoryDeleteV1
from .sync_memory_v1 import SyncMemoryV1
from .sync_memory_v1_data import SyncMemoryV1Data
from .sync_partner_delete_v1 import SyncPartnerDeleteV1
from .sync_partner_v1 import SyncPartnerV1
from .sync_person_delete_v1 import SyncPersonDeleteV1
from .sync_person_v1 import SyncPersonV1
from .sync_request_type import SyncRequestType
from .sync_reset_v1 import SyncResetV1
from .sync_stack_delete_v1 import SyncStackDeleteV1
from .sync_stack_v1 import SyncStackV1
from .sync_stream_dto import SyncStreamDto
from .sync_user_delete_v1 import SyncUserDeleteV1
from .sync_user_metadata_delete_v1 import SyncUserMetadataDeleteV1
from .sync_user_metadata_v1 import SyncUserMetadataV1
from .sync_user_metadata_v1_value import SyncUserMetadataV1Value
from .sync_user_v1 import SyncUserV1
from .system_config_backups_dto import SystemConfigBackupsDto
from .system_config_dto import SystemConfigDto
from .system_config_f_fmpeg_dto import SystemConfigFFmpegDto
from .system_config_faces_dto import SystemConfigFacesDto
from .system_config_generated_fullsize_image_dto import (
    SystemConfigGeneratedFullsizeImageDto,
)
from .system_config_generated_image_dto import SystemConfigGeneratedImageDto
from .system_config_image_dto import SystemConfigImageDto
from .system_config_job_dto import SystemConfigJobDto
from .system_config_library_dto import SystemConfigLibraryDto
from .system_config_library_scan_dto import SystemConfigLibraryScanDto
from .system_config_library_watch_dto import SystemConfigLibraryWatchDto
from .system_config_logging_dto import SystemConfigLoggingDto
from .system_config_machine_learning_dto import SystemConfigMachineLearningDto
from .system_config_map_dto import SystemConfigMapDto
from .system_config_metadata_dto import SystemConfigMetadataDto
from .system_config_new_version_check_dto import SystemConfigNewVersionCheckDto
from .system_config_nightly_tasks_dto import SystemConfigNightlyTasksDto
from .system_config_notifications_dto import SystemConfigNotificationsDto
from .system_config_o_auth_dto import SystemConfigOAuthDto
from .system_config_password_login_dto import SystemConfigPasswordLoginDto
from .system_config_reverse_geocoding_dto import SystemConfigReverseGeocodingDto
from .system_config_server_dto import SystemConfigServerDto
from .system_config_smtp_dto import SystemConfigSmtpDto
from .system_config_smtp_transport_dto import SystemConfigSmtpTransportDto
from .system_config_storage_template_dto import SystemConfigStorageTemplateDto
from .system_config_template_emails_dto import SystemConfigTemplateEmailsDto
from .system_config_template_storage_option_dto import (
    SystemConfigTemplateStorageOptionDto,
)
from .system_config_templates_dto import SystemConfigTemplatesDto
from .system_config_theme_dto import SystemConfigThemeDto
from .system_config_trash_dto import SystemConfigTrashDto
from .system_config_user_dto import SystemConfigUserDto
from .tag_bulk_assets_dto import TagBulkAssetsDto
from .tag_bulk_assets_response_dto import TagBulkAssetsResponseDto
from .tag_create_dto import TagCreateDto
from .tag_response_dto import TagResponseDto
from .tag_update_dto import TagUpdateDto
from .tag_upsert_dto import TagUpsertDto
from .tags_response import TagsResponse
from .tags_update import TagsUpdate
from .template_dto import TemplateDto
from .template_response_dto import TemplateResponseDto
from .test_email_response_dto import TestEmailResponseDto
from .time_bucket_asset_response_dto import TimeBucketAssetResponseDto
from .time_buckets_response_dto import TimeBucketsResponseDto
from .tone_mapping import ToneMapping
from .transcode_hw_accel import TranscodeHWAccel
from .transcode_policy import TranscodePolicy
from .trash_response_dto import TrashResponseDto
from .update_album_dto import UpdateAlbumDto
from .update_album_user_dto import UpdateAlbumUserDto
from .update_asset_dto import UpdateAssetDto
from .update_library_dto import UpdateLibraryDto
from .usage_by_user_dto import UsageByUserDto
from .user_admin_create_dto import UserAdminCreateDto
from .user_admin_delete_dto import UserAdminDeleteDto
from .user_admin_response_dto import UserAdminResponseDto
from .user_admin_update_dto import UserAdminUpdateDto
from .user_avatar_color import UserAvatarColor
from .user_license import UserLicense
from .user_metadata_key import UserMetadataKey
from .user_preferences_response_dto import UserPreferencesResponseDto
from .user_preferences_update_dto import UserPreferencesUpdateDto
from .user_response_dto import UserResponseDto
from .user_status import UserStatus
from .user_update_me_dto import UserUpdateMeDto
from .validate_access_token_response_dto import ValidateAccessTokenResponseDto
from .validate_library_dto import ValidateLibraryDto
from .validate_library_import_path_response_dto import (
    ValidateLibraryImportPathResponseDto,
)
from .validate_library_response_dto import ValidateLibraryResponseDto
from .version_check_state_response_dto import VersionCheckStateResponseDto
from .video_codec import VideoCodec
from .video_container import VideoContainer

__all__ = (
    "ActivityCreateDto",
    "ActivityResponseDto",
    "ActivityStatisticsResponseDto",
    "AddUsersDto",
    "AdminOnboardingUpdateDto",
    "AlbumResponseDto",
    "AlbumsAddAssetsDto",
    "AlbumsAddAssetsResponseDto",
    "AlbumsResponse",
    "AlbumStatisticsResponseDto",
    "AlbumsUpdate",
    "AlbumUserAddDto",
    "AlbumUserCreateDto",
    "AlbumUserResponseDto",
    "AlbumUserRole",
    "AllJobStatusResponseDto",
    "APIKeyCreateDto",
    "APIKeyCreateResponseDto",
    "APIKeyResponseDto",
    "APIKeyUpdateDto",
    "AssetBulkDeleteDto",
    "AssetBulkUpdateDto",
    "AssetBulkUploadCheckDto",
    "AssetBulkUploadCheckItem",
    "AssetBulkUploadCheckResponseDto",
    "AssetBulkUploadCheckResult",
    "AssetBulkUploadCheckResultAction",
    "AssetBulkUploadCheckResultReason",
    "AssetDeltaSyncDto",
    "AssetDeltaSyncResponseDto",
    "AssetFaceCreateDto",
    "AssetFaceDeleteDto",
    "AssetFaceResponseDto",
    "AssetFaceUpdateDto",
    "AssetFaceUpdateItem",
    "AssetFaceWithoutPersonResponseDto",
    "AssetFullSyncDto",
    "AssetIdsDto",
    "AssetIdsResponseDto",
    "AssetIdsResponseDtoError",
    "AssetJobName",
    "AssetJobsDto",
    "AssetMediaCreateDto",
    "AssetMediaReplaceDto",
    "AssetMediaResponseDto",
    "AssetMediaSize",
    "AssetMediaStatus",
    "AssetMetadataKey",
    "AssetMetadataResponseDto",
    "AssetMetadataResponseDtoValue",
    "AssetMetadataUpsertDto",
    "AssetMetadataUpsertItemDto",
    "AssetMetadataUpsertItemDtoValue",
    "AssetOrder",
    "AssetResponseDto",
    "AssetStackResponseDto",
    "AssetStatsResponseDto",
    "AssetTypeEnum",
    "AssetVisibility",
    "AudioCodec",
    "AuthStatusResponseDto",
    "AvatarUpdate",
    "BulkIdErrorReason",
    "BulkIdResponseDto",
    "BulkIdResponseDtoError",
    "BulkIdsDto",
    "CastResponse",
    "CastUpdate",
    "ChangePasswordDto",
    "CheckExistingAssetsDto",
    "CheckExistingAssetsResponseDto",
    "CLIPConfig",
    "Colorspace",
    "CQMode",
    "CreateAlbumDto",
    "CreateLibraryDto",
    "CreateProfileImageDto",
    "CreateProfileImageResponseDto",
    "DatabaseBackupConfig",
    "DownloadArchiveInfo",
    "DownloadInfoDto",
    "DownloadResponse",
    "DownloadResponseDto",
    "DownloadUpdate",
    "DuplicateDetectionConfig",
    "DuplicateResponseDto",
    "EmailNotificationsResponse",
    "EmailNotificationsUpdate",
    "ExifResponseDto",
    "FaceDto",
    "FacialRecognitionConfig",
    "FoldersResponse",
    "FoldersUpdate",
    "ImageFormat",
    "JobCommand",
    "JobCommandDto",
    "JobCountsDto",
    "JobCreateDto",
    "JobName",
    "JobSettingsDto",
    "JobStatusDto",
    "LibraryResponseDto",
    "LibraryStatsResponseDto",
    "LicenseKeyDto",
    "LicenseResponseDto",
    "LoginCredentialDto",
    "LoginResponseDto",
    "LogLevel",
    "LogoutResponseDto",
    "MachineLearningAvailabilityChecksDto",
    "ManualJobName",
    "MapMarkerResponseDto",
    "MapReverseGeocodeResponseDto",
    "MemoriesResponse",
    "MemoriesUpdate",
    "MemoryCreateDto",
    "MemoryResponseDto",
    "MemoryStatisticsResponseDto",
    "MemoryType",
    "MemoryUpdateDto",
    "MergePersonDto",
    "MetadataSearchDto",
    "NotificationCreateDto",
    "NotificationCreateDtoData",
    "NotificationDeleteAllDto",
    "NotificationDto",
    "NotificationDtoData",
    "NotificationLevel",
    "NotificationType",
    "NotificationUpdateAllDto",
    "NotificationUpdateDto",
    "OAuthAuthorizeResponseDto",
    "OAuthCallbackDto",
    "OAuthConfigDto",
    "OAuthTokenEndpointAuthMethod",
    "OnboardingDto",
    "OnboardingResponseDto",
    "OnThisDayDto",
    "PartnerCreateDto",
    "PartnerDirection",
    "PartnerResponseDto",
    "PartnerUpdateDto",
    "PeopleResponse",
    "PeopleResponseDto",
    "PeopleUpdate",
    "PeopleUpdateDto",
    "PeopleUpdateItem",
    "Permission",
    "PersonCreateDto",
    "PersonResponseDto",
    "PersonStatisticsResponseDto",
    "PersonUpdateDto",
    "PersonWithFacesResponseDto",
    "PinCodeChangeDto",
    "PinCodeResetDto",
    "PinCodeSetupDto",
    "PlacesResponseDto",
    "PurchaseResponse",
    "PurchaseUpdate",
    "QueueStatusDto",
    "RandomSearchDto",
    "RatingsResponse",
    "RatingsUpdate",
    "ReactionLevel",
    "ReactionType",
    "ReverseGeocodingStateResponseDto",
    "SearchAlbumResponseDto",
    "SearchAssetResponseDto",
    "SearchExploreItem",
    "SearchExploreResponseDto",
    "SearchFacetCountResponseDto",
    "SearchFacetResponseDto",
    "SearchResponseDto",
    "SearchStatisticsResponseDto",
    "SearchSuggestionType",
    "ServerAboutResponseDto",
    "ServerApkLinksDto",
    "ServerConfigDto",
    "ServerFeaturesDto",
    "ServerMediaTypesResponseDto",
    "ServerPingResponse",
    "ServerStatsResponseDto",
    "ServerStorageResponseDto",
    "ServerThemeDto",
    "ServerVersionHistoryResponseDto",
    "ServerVersionResponseDto",
    "SessionCreateDto",
    "SessionCreateResponseDto",
    "SessionResponseDto",
    "SessionUnlockDto",
    "SessionUpdateDto",
    "SharedLinkCreateDto",
    "SharedLinkEditDto",
    "SharedLinkResponseDto",
    "SharedLinksResponse",
    "SharedLinksUpdate",
    "SharedLinkType",
    "SignUpDto",
    "SmartSearchDto",
    "SourceType",
    "StackCreateDto",
    "StackResponseDto",
    "StackUpdateDto",
    "StatisticsSearchDto",
    "SyncAckDeleteDto",
    "SyncAckDto",
    "SyncAckSetDto",
    "SyncAckV1",
    "SyncAlbumDeleteV1",
    "SyncAlbumToAssetDeleteV1",
    "SyncAlbumToAssetV1",
    "SyncAlbumUserDeleteV1",
    "SyncAlbumUserV1",
    "SyncAlbumV1",
    "SyncAssetDeleteV1",
    "SyncAssetExifV1",
    "SyncAssetFaceDeleteV1",
    "SyncAssetFaceV1",
    "SyncAssetMetadataDeleteV1",
    "SyncAssetMetadataV1",
    "SyncAssetMetadataV1Value",
    "SyncAssetV1",
    "SyncAuthUserV1",
    "SyncCompleteV1",
    "SyncEntityType",
    "SyncMemoryAssetDeleteV1",
    "SyncMemoryAssetV1",
    "SyncMemoryDeleteV1",
    "SyncMemoryV1",
    "SyncMemoryV1Data",
    "SyncPartnerDeleteV1",
    "SyncPartnerV1",
    "SyncPersonDeleteV1",
    "SyncPersonV1",
    "SyncRequestType",
    "SyncResetV1",
    "SyncStackDeleteV1",
    "SyncStackV1",
    "SyncStreamDto",
    "SyncUserDeleteV1",
    "SyncUserMetadataDeleteV1",
    "SyncUserMetadataV1",
    "SyncUserMetadataV1Value",
    "SyncUserV1",
    "SystemConfigBackupsDto",
    "SystemConfigDto",
    "SystemConfigFacesDto",
    "SystemConfigFFmpegDto",
    "SystemConfigGeneratedFullsizeImageDto",
    "SystemConfigGeneratedImageDto",
    "SystemConfigImageDto",
    "SystemConfigJobDto",
    "SystemConfigLibraryDto",
    "SystemConfigLibraryScanDto",
    "SystemConfigLibraryWatchDto",
    "SystemConfigLoggingDto",
    "SystemConfigMachineLearningDto",
    "SystemConfigMapDto",
    "SystemConfigMetadataDto",
    "SystemConfigNewVersionCheckDto",
    "SystemConfigNightlyTasksDto",
    "SystemConfigNotificationsDto",
    "SystemConfigOAuthDto",
    "SystemConfigPasswordLoginDto",
    "SystemConfigReverseGeocodingDto",
    "SystemConfigServerDto",
    "SystemConfigSmtpDto",
    "SystemConfigSmtpTransportDto",
    "SystemConfigStorageTemplateDto",
    "SystemConfigTemplateEmailsDto",
    "SystemConfigTemplatesDto",
    "SystemConfigTemplateStorageOptionDto",
    "SystemConfigThemeDto",
    "SystemConfigTrashDto",
    "SystemConfigUserDto",
    "TagBulkAssetsDto",
    "TagBulkAssetsResponseDto",
    "TagCreateDto",
    "TagResponseDto",
    "TagsResponse",
    "TagsUpdate",
    "TagUpdateDto",
    "TagUpsertDto",
    "TemplateDto",
    "TemplateResponseDto",
    "TestEmailResponseDto",
    "TimeBucketAssetResponseDto",
    "TimeBucketsResponseDto",
    "ToneMapping",
    "TranscodeHWAccel",
    "TranscodePolicy",
    "TrashResponseDto",
    "UpdateAlbumDto",
    "UpdateAlbumUserDto",
    "UpdateAssetDto",
    "UpdateLibraryDto",
    "UsageByUserDto",
    "UserAdminCreateDto",
    "UserAdminDeleteDto",
    "UserAdminResponseDto",
    "UserAdminUpdateDto",
    "UserAvatarColor",
    "UserLicense",
    "UserMetadataKey",
    "UserPreferencesResponseDto",
    "UserPreferencesUpdateDto",
    "UserResponseDto",
    "UserStatus",
    "UserUpdateMeDto",
    "ValidateAccessTokenResponseDto",
    "ValidateLibraryDto",
    "ValidateLibraryImportPathResponseDto",
    "ValidateLibraryResponseDto",
    "VersionCheckStateResponseDto",
    "VideoCodec",
    "VideoContainer",
)
