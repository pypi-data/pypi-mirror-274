import argparse
import requests
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json
from typing import Any, Optional, List
from urllib.parse import urlencode
from functools import wraps
import datetime
import json
from types import SimpleNamespace

base_url = "https://api.curseforge.com"

def JsonToType(data):
    """
    Transform API response to python type
    """
    return(json.loads(data, object_hook=lambda d: SimpleNamespace(**d)))

class req_method(Enum):
    GET = 0
    POST = 1

GET = req_method.GET
POST = req_method.POST

@dataclass
class endpoint:
    method: req_method
    endpoint: Path
    description: Optional[str] = None

endpoints = {
    #Games
    "games":endpoint(GET, '/v1/games', 'Get all games that are available to the provided API key.'),
    "game":endpoint(GET, '/v1/games/{gameId}', 'Get a single game. A private game is only accessible by its respective API key.'),
    "versions":endpoint(GET, '/v2/games/{gameId}/versions', 'Get all available versions for each known version type of the specified game. A private game is only accessible to its respective API key.'),
    "version_types":endpoint(GET,'/v1/games/{gameId}/version-types','Get all available version types of the specified game.'),
    #Categories
    "categories":endpoint(GET, '/v1/categories?', "Get all available classes and categories of the specified game. Specify a game id for a list of all game categories, or a class id for a list of categories under that class. specifiy the classes Only flag to just get the classes for a given game."),
    #Mods
    "search_mods":endpoint(GET, '/v1/mods/search?','Get all mods that match the search criteria.'),
    "get_mod":endpoint(GET, '/v1/mods/{modId}', 'Get a single mod.'),
    "get_mods":endpoint(POST, '/v1/mods', 'Get a list of mods belonging the the same game.'),
    "get_featured_mods":endpoint(POST, '/v1/mods/featured', 'Get a list of featured, popular and recently updated mods.'),
    "get_mod_description":endpoint(GET, '/v1/mods/{modId}/description', 'Get the full description of a mod in HTML format.'),
    #Files
    "get_mod_file":endpoint(GET,'/v1/mods/{modId}/files/{fileId}','Get a single file of the specified mod.'),
    "get_mod_files":endpoint(GET,'/v1/mods/{modId}/files','Get all files of the specified mod.'),
    "get_files":endpoint(POST, '/v1/mods/files', 'Get a list of files.'),
    "get_mod_file_changelog":endpoint(GET, '/v1/mods/{modId}/files/{fileId}/changelog', 'Get the changelog of a file in HTML format.'),
    "get_mod_file_download_url":endpoint(GET, '/v1/mods/{modId}/files/{fileId}/download-url', 'Get a download url for a specific file.'),
    #Minecraft
    "get_minecraft_versions":endpoint(GET,'/v1/minecraft/version',''),
    "get_specific_minecraft_version":endpoint(GET,'/v1/minecraft/version/{gameVersionString}',''),
    "get_minecraft_modloaders":endpoint(GET,'/v1/minecraft/modloader',''),
    "get_specific_minecraft_modloader":endpoint(GET,'/v1/minecraft/modloader/{modLoaderName}','')
    #Fingerprints ???
}

@dataclass
class ApiResponseOf:
    data: Any
GetResponse = ApiResponseOf # Alias

@dataclass
class Pagination:
    index: int
    pageSize: int
    resultCount: int
    totalCount: int

@dataclass
class GetResponseWithPagination:
    data: Any
    pagination: Pagination

class ModsSearchSortField(Enum):
    Featured = 1
    Popularity = 2
    LastUpdated = 3
    Name = 4
    Author = 5
    TotalDownloads = 6
    Category = 7
    GameVersion = 8
    EarlyAccess = 9
    FeaturedReleased = 10
    ReleasedDate = 11
    Rating = 12

class ModLoaderType(Enum):
    Any = 0
    Forge = 1
    Cauldron = 2
    LiteLoader = 3
    Fabric = 4
    Quilt = 5
    NeoForge = 6

class SortOrder(str, Enum):
    Ascending = 'asc'
    Descending = 'desc'

class GameVersionTypeStatus(Enum):
    Normal = 1
    Deleted = 2

class GameVersionStatus(Enum):
    Approved = 1
    Deleted = 2
    New = 3

@dataclass
class GameVersionType:
    id: int
    gameId: int
    name: str
    slug: str
    isSyncable: bool
    status: GameVersionTypeStatus

@dataclass
class MinecraftGameVersion:
    id: int
    gameVersionId: int
    versionString: str
    jarDownloadUrl: str
    jsonDownloadUrl: str
    approved: bool
    dateModified: datetime.datetime
    gameVersionTypeId: int
    gameVersionStatus: GameVersionStatus
    gameVersionTypeStatus: GameVersionTypeStatus

@dataclass
class Category:
    id: int
    gameId: int
    name: str
    slug: str
    url: str
    iconUrl: str
    dateModified: datetime.datetime
    isClass: Optional[bool] = None
    classId: Optional[int] = None
    parentCategoryId: Optional[int] = None
    displayIndex: Optional[int] = None

class CoreApiStatus(Enum):
    Private = 1
    Public = 2

class CoreStatus(Enum):
    Draft = 1
    Test = 2
    PendingReview = 3
    Rejected = 4
    Approved = 5
    Live = 6

@dataclass
class ModLinks:
    websiteUrl: str
    wikiUrl: str
    issuesUrl: str
    sourceUrl: str

class ModStatus(Enum):
    New = 1
    ChangesRequired = 2
    UnderSoftReview = 3
    Approved = 4
    Rejected = 5
    ChangesMade = 6
    Inactive = 7
    Abandoned = 8
    Deleted = 9
    UnderReview = 10

@dataclass
class ModAuthor:
    id: int
    name: str
    url: str

@dataclass
class ModAsset:
    id: int
    modId: int
    title: str
    description: str
    thumbnailUrl: str
    url: str

class FileReleaseType(Enum):
    Release = 1
    Beta = 2
    Alpha = 3

class FileStatus(Enum):
    Processing = 1
    ChangesRequired = 2
    UnderReview = 3
    Approved = 4
    Rejected = 5
    MalwareDetected = 6
    Deleted = 7
    Archived = 8
    Testing = 9
    Released = 10
    ReadyForReview = 11
    Deprecated = 12
    Baking = 13
    AwaitingPublishing = 14
    FailedPublishing = 15

class HashAlgo(Enum):
    Sha1 = 1
    Md5 = 2

@dataclass
class FileHash:
    value: str
    algo: HashAlgo

@dataclass
class SortableGameVersion:
    gameVersionName: str
    gameVersionPadded: str
    gameVersion: str
    gameVersionReleaseDate: datetime.datetime
    gameVersionTypeId: Optional[int] = None

class FileRelationType(Enum):
    EmbeddedLibrary = 1
    OptionalDependency = 2
    RequiredDependency = 3
    Tool = 4
    Incompatible = 5
    Include = 6

@dataclass
class FileDependency:
    modId: int
    relationType: FileRelationType

@dataclass
class FileModule:
    name: str
    fingerprint: int

@dataclass
class File:
    id: int
    gameId: int
    modId: int
    isAvailable: bool
    displayName: str
    fileName: str
    releaseType: FileReleaseType
    fileStatus: FileStatus
    hashes: list[FileHash]
    fileDate: datetime.datetime
    fileLength: int
    downloadCount: int
    downloadUrl: str
    gameVersions: list[str]
    sortableGameVersions: list[SortableGameVersion]
    dependencies: list[FileDependency]
    fileFingerprint: int
    modules: list[FileModule]
    earlyAccessEndDate: Optional[datetime.datetime] = None
    exposeAsAlternative: Optional[bool] = None
    parentProjectFileId: Optional[int] = None
    alternateFileId: Optional[int] = None
    isServerPack: Optional[bool] = None
    serverPackFileId: Optional[int] = None
    isEarlyAccessContent: Optional[bool] = None
    fileSizeOnDisk: Optional[int] = None


@dataclass
class FileIndex:
    gameVersion: str
    fileId: int
    filename: str
    releaseType: FileReleaseType
    modLoader: Optional[ModLoaderType] = None
    gameVersionTypeId: Optional[int] = None

@dataclass
class Mod:
    id: int
    gameId: int
    name: str
    slug: str
    links: ModLinks
    summary: str
    status: ModStatus
    downloadCount: int
    isFeatured: bool
    primaryCategoryId: int
    categories: list[Category]
    authors: list[ModAuthor]
    logo: ModAsset
    screenshots: list[ModAsset]
    mainFileId: int
    latestFiles: list[File]
    latestFilesIndexes: list[FileIndex]
    latestEarlyAccessFilesIndexes: list[FileIndex]
    dateCreated: datetime.datetime
    dateModified: datetime.datetime
    dateReleased: datetime.datetime
    gamePopularityRank: int
    isAvailable: bool
    thumbsUpCount: int
    classId: Optional[int] = None
    rating: Optional[int] = None
    allowModDistribution: Optional[bool] = None

@dataclass
class FeaturedModsResponse:
    featured: list[Mod]
    popular: list[Mod]
    recentlyUpdated: list[Mod]

@dataclass
class FingerprintFuzzyMatch:
    id: int
    file: File
    latestFiles: list[File]
    fingerprints: list[int]

@dataclass
class FingerprintFuzzyMatchResult:
    fuzzyMatches: list[FingerprintFuzzyMatch]

@dataclass
class FingerprintMatch:
    id: int
    file: File
    latestFiles: list[File]

@dataclass
class FingerprintsMatchesResult:
    isCacheBuilt: bool
    exactMatches: list[FingerprintMatch]
    exactFingerprints: list[int]
    partialMatches: list[FingerprintMatch]
    partialMatchFingerprints: object
    additionalProperties: list[int]
    installedFingerprints: list[int]
    unmatchedFingerprints: list[int]

@dataclass
class FolderFingerprint:
    foldername: str
    fingerprints: list[int]

@dataclass
class GameAssets:
    iconUrl: str
    tileUrl: str
    coverUrl: str

@dataclass
class Game:
    id: int
    name: str
    slug: str
    dateModified: datetime.datetime
    assets: GameAssets
    status: CoreStatus
    apiStatus: CoreApiStatus

@dataclass
class GameVersion:
    id: int
    slug: str
    name: str
    
@dataclass
class GameVersionsByType:
    type: int
    versions: list[str]

@dataclass
class GameVersionsByType2:
    type: int
    versions: list[GameVersion]

@dataclass
class GetFeaturedModsRequessstBody:
    gameId: int
    excludedModIds: list[int]
    gameVerssionTypeId: Optional[int] = None

@dataclass
class GetFingerprintMatchesRequestBody:
    fingerprints: list[int]

@dataclass
class GetFuzzyMatchesRequestBody:
    gameId: int
    fingerprints: list[FolderFingerprint]

@dataclass
class GetModFilesRequestBody:
    fields: list[int]

@dataclass
class GetModsByIdsListRequestBody:
    modIdss: list[int]
    filterPcOnly: Optional[bool] = None

@dataclass
class MinecraftModLoaderIndex:
    name: str
    gameVersion: str
    latest: bool
    recommended: bool
    dateModified: datetime.datetime
    type: ModLoaderType

class ModLoaderInstallMethod(Enum):
    ForgeInstaller = 1
    ForgeJarInstall = 2
    ForgeInstaller_v2 = 3

@dataclass
class MinecraftModLoaderVersion:
    id: int
    gameVersionId: int
    forgeVersion: str
    name: str
    type: ModLoaderType
    downloadUrl: str
    filename: str
    installMethod: ModLoaderInstallMethod
    latest: bool
    recommended: bool
    approved: bool
    dateModified: datetime.datetime
    maverVersionString: str
    versionJson: str
    librariesInstallLocation: str
    minecraftVersion: str
    additionalFilessJson: str
    modLoaderGameVersionId: int
    modLoaderGameVersionTypeId: int
    modLoaderGameVersionStatuss: GameVersionStatus
    modLoaderGameVersionTypeStatus: GameVersionTypeStatus
    mcGameVersionId: int
    mcGameVersionTypeId: int
    mcGameVersionStatus: GameVersionStatus
    mcGameVersionTypeStatus: GameVersionTypeStatus
    installProfileJson: str