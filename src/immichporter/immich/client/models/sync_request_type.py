from enum import Enum


class SyncRequestType(str, Enum):
    ALBUMASSETEXIFSV1 = "AlbumAssetExifsV1"
    ALBUMASSETSV1 = "AlbumAssetsV1"
    ALBUMSV1 = "AlbumsV1"
    ALBUMTOASSETSV1 = "AlbumToAssetsV1"
    ALBUMUSERSV1 = "AlbumUsersV1"
    ASSETEXIFSV1 = "AssetExifsV1"
    ASSETFACESV1 = "AssetFacesV1"
    ASSETMETADATAV1 = "AssetMetadataV1"
    ASSETSV1 = "AssetsV1"
    AUTHUSERSV1 = "AuthUsersV1"
    MEMORIESV1 = "MemoriesV1"
    MEMORYTOASSETSV1 = "MemoryToAssetsV1"
    PARTNERASSETEXIFSV1 = "PartnerAssetExifsV1"
    PARTNERASSETSV1 = "PartnerAssetsV1"
    PARTNERSTACKSV1 = "PartnerStacksV1"
    PARTNERSV1 = "PartnersV1"
    PEOPLEV1 = "PeopleV1"
    STACKSV1 = "StacksV1"
    USERMETADATAV1 = "UserMetadataV1"
    USERSV1 = "UsersV1"

    def __str__(self) -> str:
        return str(self.value)
