# -*- coding: utf-8 -*-
import os
import pickle
import shutil
import logging
import requests
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..util.api import run_api_query
from ..util.exception import OxaigenSDKException

S3_ASSET_DOWNLOAD_LINK = "getS3AssetDownloadLink"
FILE_NAME = "fileName"
FILE_SIZE = "fileSize"
FILE_TYPE = "fileType"
DOWNLOAD_URL = "downloadUrl"
LAST_MODIFIED = "lastModified"


class OxaigenAsset:
    """
    Oxaigen Asset class
    """

    def __init__(self):
        super().__init__()

    def get_asset(
            self,
            asset_key: List[str],
            file_path: str,
            run_id: Optional[str] = None,
            use_cache: bool = True
    ) -> Optional[Any]:
        """
        Download an Asset from the Oxaigen Orchestration data plane
        """
        if use_cache:
            return self._get_asset_from_cache(asset_key=asset_key, file_path=file_path, run_id=run_id)
        else:
            return self.download_asset(asset_key=asset_key, file_path=file_path, run_id=run_id)

    def _get_asset_from_cache(
            self,
            asset_key: List[str],
            file_path: str,
            run_id: Optional[str] = None
    ) -> Optional[Any]:
        """
        Function to get an Asset from the DataPlane from cache (local file storage)
        """
        data = _get_download_asset_link(asset_key=asset_key, run_id=run_id)
        file_name = data[S3_ASSET_DOWNLOAD_LINK][FILE_NAME]
        file = os.path.join(file_path, file_name)

        # FUTURE TODO: if file remote is "newer" then cache file or file size differences, download
        last_modified = data[S3_ASSET_DOWNLOAD_LINK][LAST_MODIFIED]

        asset = _get_asset_from_file(file=file)

        # fallback to fresh download
        if not asset:
            return self.download_asset(asset_key=asset_key, file_path=file_path, run_id=run_id)

    def download_asset(
            self,
            asset_key: List[str],
            file_path: Optional[str] = None,
            run_id: Optional[str] = None
    ) -> Optional[Any]:
        """
        Download an Asset from the Oxaigen Orchestration data plane
        """
        if not file_path:
            file_path = asset_key  # TODO: turn this into a path: ["asdf","jkl"] into "asdf/jkl" starting from HOME!
        try:
            data = _get_download_asset_link(asset_key=asset_key, run_id=run_id)
            url = data[S3_ASSET_DOWNLOAD_LINK][DOWNLOAD_URL]
            file_name = data[S3_ASSET_DOWNLOAD_LINK][FILE_NAME]
            file_size = data[S3_ASSET_DOWNLOAD_LINK][FILE_SIZE]

            logging.info(msg=f"Downloading file {file_name} ({file_size}) into this directory: {file_path}")
            _download_asset_file(url=url, file_path=file_path, file_name=file_name)

            file = os.path.join(file_path, file_name)
            asset = _get_asset_from_file(file=file)

            if not asset:
                raise OxaigenSDKException(message=f"Could not open downloaded asset, try again")

            return asset

        except Exception as e:
            raise OxaigenSDKException(message=f"Could not download asset, Error: {str(e)}")


def _get_download_asset_link(
        asset_key: List[str],
        run_id: Optional[str]
) -> Optional[Dict]:
    """
    Function to get a temporary download link from the Oxaigen Client API to a file in the Oxaigen data plane
    """
    if not run_id:
        run_id = ""

    query = """
            query GetDownloadLink($assetKey: [String!]!, $runId: String = "") {
              getS3AssetDownloadLink(assetKey: $assetKey, runId: $runId) {
                ... on AssetDownloadLink {
                  __typename
                  downloadUrl
                  fileSize
                  fileType
                  lastModified
                }
                ... on AssetNotFound {
                  __typename
                  errorMessage
                }
                ... on AssetDownloadError {
                  __typename
                  errorMessage
                }
                ... on AuthenticationError {
                  __typename
                  errorMessage
                }
                ... on AuthorizationError {
                  __typename
                  errorMessage
                }
              }
            }
            """

    variables = {
        "assetKey": asset_key,
        "runId": run_id
    }

    return run_api_query(query=query, variables=variables)


def _download_asset_file(url: str, file_path: str, file_name: str):
    """
    Function to download a file from bucket storage system using an S3 generated URL (with one-time-use credentials)
    """
    # Create directory if it doesn't exist
    os.makedirs(file_path, exist_ok=True)

    # Full file path
    full_file_path = os.path.join(file_path, file_name)

    # Check if file exists
    if os.path.exists(full_file_path):
        file_size_mb = os.path.getsize(full_file_path) / (1024 * 1024)
        if file_size_mb < 200:
            backup_name = f"{file_name}__backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path = os.path.join(file_path, backup_name)
            shutil.move(full_file_path, backup_path)
        else:
            logging.warning(msg=f"Existing asset size ({str(file_size_mb)}) to large (>200mb), will not create backup")

    # Download the file
    response = requests.get(url, stream=True)
    with open(full_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def _get_asset_from_file(file: str) -> Optional[Any]:
    """
    get an Asset from the Oxaigen Orchestration data plane from the internal User Cache
    """
    try:
        with open(file, 'rb') as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        logging.warning(msg=f"Error reading asset file ({str(file)}) from disk. Error: {str(e)}")
        return None
