#!/bin/python3
import argparse
import requests
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json
from typing import Any, Optional, List
from urllib.parse import urlencode
from functools import wraps
from dataclass_wizard import fromdict, asdict
import colorama

from tools.types import *

DEBUG = False
REQUEST = True

#Test API token used by official curseforge apps
import base64
CFApiKey = base64.b64decode("JDJhJDEwJGJMNGJJTDVwVVdxZmNPN0tRdG5NUmVha3d0ZkhiTktoNnYxdVRwS2x6aHdvdWVFSlFuUG5t").decode('utf-8')

class CFAPI:
    """
    Base class for CurseForge API
    """
    def __init__(self, api_key):
        self.api_key = api_key
    def cf_get(self, endpoint_url: str):
        if DEBUG: print(f'GET: {base_url+endpoint_url}')
        return requests.get(url=base_url+endpoint_url, headers={
            'Accept': 'application/json',
            'x-api-key': self.api_key})
    def cf_post(self, endpoint_url, data):
        if DEBUG: print(f'POST: {base_url+endpoint_url}\nDATA: {data}')
        return requests.post(url=base_url+endpoint_url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-api-key': self.api_key}, data=data)
    def cf_api(self, endpoint: endpoint, data: Optional[object] = None, params: Optional[dict] = None, query: Optional[dict] = None):
        """
        Call to curseforge API
        :param endpoint:  Endpoint class with `endpoint` string, request method and endpoint description inside it. Predefined in `endpoints` variable.
        :param data: Data sent to server, POST only. (cf_post)
        :param params: `!!MANDATORY!!` Params to substitute in endpoint string
        :param query: Url query
        """
        method = endpoint.method
        if data: data = json.dumps(data)
        if query: 
            query = urlencode(query)
        else:
            query = ""
        endpoint_url = str(endpoint.endpoint)+query
        if DEBUG:
            d_str = 'endpoint: {endpoint_url}\napi_key:{api_key}\ndata:{data}\nparams:{params}\nquery:{query}'.format(
                endpoint_url = endpoint_url,
                api_key = self.api_key,
                data = data,
                params = params,
                query = query
            )
            print(d_str)
        if REQUEST:
            if params:
                endpoint_url = endpoint_url.format(**params)
            if method == GET:
                return(self.cf_get(endpoint_url))
            if method == POST:
                return(self.cf_post(endpoint_url, data))

class CFGames(CFAPI):
    #!! Add apgination parameters
    def games(self) -> tuple[list[Game], Pagination]:
        """
        Get all games that are available to the provided API key.
        """
        response = json.loads(self.cf_api(endpoints["games"]).text)
        pagination = Pagination(**response['pagination'])
        data = [fromdict(Game, game) for game in response['data']]
        return(data, pagination)
    def game(self, gameId) -> Game:
        """
        Get a single game.
        A private game is only accessible by its respective API key.
        """
        response = json.loads(self.cf_api(endpoints["game"], params={"gameId":gameId}).text)
        print(response)
        data = fromdict(Game, response['data'])
        return(data)
    def versions(self, gameId) -> list[GameVersionsByType]:
        """
        Get all available versions for each known version type of the specified game.
        A private game is only accessible to its respective API key.
        """
        response = json.loads(self.cf_api(endpoints["versions"], params={"gameId":gameId}).text)
        data = [fromdict(GameVersionsByType, vbt) for vbt in response['data']]
        return(data)
    def version_types(self, gameId) -> list[GameVersionType]:
        """
        Get all available version types of the specified game.
        A private game is only accessible to its respective API key.
        Currently, when creating games via the CurseForge for Studios Console, you are limited to a single game version type.
        This means that this endpoint is probably not useful in most cases and is relevant mostly when handling existing games that have multiple game versions such as World of Warcraft and Minecraft (e.g. 517 for wow_retail).
        """
        response = json.loads(self.cf_api(endpoints["version_types"], params={"gameId":gameId}).text)
        data = [fromdict(GameVersionType, gvt) for gvt in response['data']]
        return(data)

class CFCategories(CFAPI):
    def categories(self, gameId: int, classId: Optional[int] = None, classesOnly: Optional[bool] = None) -> list[Category]:
        """
        Get all available classes and categories of the specified game.
        Specify a game id for a list of all game categories, or a class id for a list of categories under that class.
        Specifiy the classes Only flag to just get the classes for a given game.
        """
        query = {"gameId":gameId}
        if classId: query['classId'] = classId
        if classesOnly: query['classesOnly'] = classesOnly
        response = json.loads(self.cf_api(endpoints["categories"],query=query).text)
        data = [fromdict(Category, category) for category in response['data']]
        return(data)

class CFMods(CFAPI):
    def search_mods(
        self, gameId: int, classId: Optional[int]=None,
        categoryId: Optional[int]=None, categoryIds: Optional[str]=None,
        gameVersion: Optional[str]=None, gameVersions: Optional[str]=None,
        searchFilter: Optional[str]=None, sortField: Optional[ModsSearchSortField]=None,
        sortOrder: Optional[SortOrder]=None, modLoaderType: Optional[ModLoaderType]=None,
        modLoaderTypes: Optional[str]=None, gameVersionTypeId: Optional[int]=None,
        authorId: Optional[int]=None, primaryAuthorId: Optional[int]=None,
        slug: Optional[str]=None, index: Optional[int]=None, pageSize: Optional[int]=None
        ) -> tuple[list[Mod], Pagination]:
        """
        Get all mods that match the search criteria.
        """
        query = {"gameId":gameId}
        # Construct optional part:
        if classId: query['classId'] = classId
        if categoryId: query['categoryId'] = categoryId
        if categoryIds: query['categoryIds'] = categoryIds
        if gameVersion: query['gameVersion'] = gameVersion
        if gameVersions: query['gameVersions'] = gameVersions 
        if searchFilter: query['searchFilter'] = searchFilter
        if sortField: query['sortField'] = sortField.value 
        if sortOrder: query['sortOrder'] = sortOrder.value
        if modLoaderType: query['modLoaderType'] = modLoaderType.value
        if gameVersionTypeId: query['gameVersionTypeId'] = gameVersionTypeId
        if authorId: query['authorId'] = authorId
        if primaryAuthorId: query['primaryAuthorId'] = primaryAuthorId
        if slug: query['slug'] = slug
        if index: query['index'] = index
        if pageSize: query['pageSize'] = pageSize
        # Call curseforge api
        response = json.loads(self.cf_api(endpoints['search_mods'], query=query).text)
        pagination = Pagination(**response['pagination'])
        data = [fromdict(Mod, moddata) for moddata in response['data']]
        return(data, pagination)

    def get_mod(self, modId: int) -> Mod:
        """
        Get a single mod.
        """
        response = json.loads(self.cf_api(endpoints['get_mod'], params={'modId':modId}).text)
        data = fromdict(Mod, response['data'])
        return(data)

    def get_mods(self, modIds: list[int], filterPCOnly: Optional[bool] = True) -> list[Mod]:
        """
        Get a list of mods belonging the the same game.
        """
        body = {"modIds":modIds}
        if filterPCOnly: body["filterPCOnly"] = filterPCOnly
        response = json.loads(self.cf_api(endpoints['get_mods'], data=body).text)
        data = [fromdict(Mod, moddata) for moddata in response['data']]
        return(data)

    def get_featured_mods(self, gameId: int, excludedModIds: Optional[List] = None, gameVersionTypeId: Optional[int] = None) -> FeaturedModsResponse:
        """
        Get a list of featured, popular and recently updated mods.
        """
        body = {"gameId":gameId}
        if excludedModIds: body['excludedModIds'] = excludedModIds
        if gameVersionTypeId: body['gameVersionTypeId'] = gameVersionTypeId
        response = json.loads(self.cf_api(endpoints['get_featured_mods'],data=body).text)
        data = fromdict(FeaturedModsResponse, response['data'])
        return(data)

    def get_mod_description(self, modId: int, raw: Optional[bool] = None, stripped: Optional[bool] = None, markup: Optional[bool] = None) -> str:
        """
        Get the full description of a mod in HTML format.
        """
        query = {"modId":modId}
        if raw: query['raw'] = raw
        if stripped: query['stripped'] = stripped
        if markup: query['markup'] = markup
        response = json.loads(self.cf_api(endpoints['get_mod_description'], query=query).text)
        data = response['data']
        return(data)

class CFFiles(CFAPI):
    def get_mod_file(self, modId: int, fileId: int) -> File:
        """
        Get a single file of the specified mod.
        """
        response = json.loads(self.cf_api(endpoints['get_mod_file'], params={'modId':modId, 'fileId':fileId}).text)
        data = fromdict(Mod, response['data'])
        return(data)

    def get_mod_files(
        self, modId: int, gameVersion: Optional[str] = None,
        modLoaderType: Optional[ModLoaderType] = None, gameVersionTypeId: Optional[int] = None,
        index: Optional[int] = None, pageSize: Optional[int] = None) -> tuple[list[File], Pagination]:
        """
        Get all files of the specified mod.
        """
        query={}
        if gameVersion: query['gameVersion'] = gameVersion
        if modLoaderType: query['modLoaderType'] = modLoaderType
        if gameVersionTypeId: query['gameVersionTypeId'] = gameVersionTypeId
        if index: query['index'] = index
        if pageSize: query['pageSize'] = pageSize
        response = json.loads(self.cf_api(endpoints['get_mod_files'],params={'modId':modId}, query=query).text)
        pagination = Pagination(**response['pagination'])
        data = [fromdict(File, f) for f in response['data']]
        return(data, pagination)

    def get_files(self, fileIds: list) -> list[File]:
        """
        Get a list of files.
        """
        body = {"fileIds":fileIds}
        response = json.loads(self.cf_api(endpoints['get_files'], data=body).text)
        data = [fromdict(File, f) for f in response['data']]
        return(data)

    def get_mod_file_changelog(self, modId: int, fileId: int) -> str:
        """
        Get the changelog of a file in HTML format.
        """
        respone = json.loads(self.cf_api(endpoints['get_mod_file_changelog'], params={'modId':modId, 'fileId':fileId}).text)
        data = response['data']
        return(data)

    def get_mod_file_download_url(self, modId: int, fileId: int) -> str:
        """
        Get a download url for a specific file.
        """
        response = json.loads(self.cf_api(endpoints['get_mod_file_download_url'], params={'modId':modId, 'fileId':fileId}).text)
        data = response['data']
        return(data)

class CFMinecraft(CFAPI):
    def get_minecraft_versions(self, sortDescending: Optional[bool] = None) -> list[MinecraftGameVersion]:
        """
        Get all Minecraft versions.
        """
        query = {}
        if sortDescending: query['sortDescending'] = sortDescending
        response = json.loads(self.cf_api(endpoints['get_minecraft_versions'], query=query).text)
        data = [MinecraftGameVersion(**mc_gv) for mc_gv in response['data']]
        data = [fromdict(MinecraftGameVersion, mc_gv) for mc_gv in response['data']]
        return(data)

    def get_specific_minecraft_version(self, gameVersionString: str) -> MinecraftGameVersion:
        """
        Get information about specific Minecraft version.
        """
        response = json.loads(self.cf_api(endpoints['get_specific_minecraft_version'], params={'gameVersionString':gameVersionString}).text)
        data = fromdict(MinecraftGameVersion, response['data'])
        return(data)

    def get_minecraft_modloaders(self, version: Optional[str] = None, includeAll: Optional[bool] = None) -> list[MinecraftModLoaderIndex]:
        """
        Get list of all Minecraft modloaders.
        """
        query={}
        if version: query['version'] = version
        if includeAll: query['includeAll'] = includeAll
        response = json.loads(self.cf_api(endpoints['get_minecraft_modloaders'], query=query).text)
        data = [fromdict(MinecraftModLoaderIndex, ml_idx) for ml_idx in response['data']]
        return(data)

    def get_specific_minecraft_modloader(self, modLoaderName: str) -> MinecraftModLoaderVersion:
        """
        Get everything about specific Minecraft modloader version.
        """
        response = json.loads(self.cf_api(endpoints['get_specific_minecraft_modloader'],params={'modLoaderName':modLoaderName}).text)
        data = fromdict(MinecraftModLoaderVersion, response['data'])
        return(data)

class CFFingerprints(CFAPI):
    """
    NOT IMPLEMENTED
    """
    pass

class CFClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.Games = CFGames(self.api_key)
        self.Categories = CFCategories(self.api_key)
        self.Mods = CFMods(self.api_key)
        self.Files = CFFiles(self.api_key)
        self.Minecraft = CFMinecraft(self.api_key)
        self.Fingerprints = CFFingerprints(self.api_key)