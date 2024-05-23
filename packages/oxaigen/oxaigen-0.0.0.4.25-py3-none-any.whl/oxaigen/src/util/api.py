# -*- coding: utf-8 -*-
import os
import requests
from typing import Dict, Any

from ..constant import ACCESS_TOKEN
from ..config import API_ENDPOINT
from .exception import OxaigenApiException
from .token import get_access_token_from_token_file


def run_api_query(query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    """
    Util function to call the Oxaigen Private Client API and handles authorization errors
    """
    try:
        access_token = os.environ.get(ACCESS_TOKEN)
        if not access_token:
            access_token = get_access_token_from_token_file()
            if not access_token:
                raise OxaigenApiException(message="No Access Token available, please login again")

        # Define the payload
        payload = {
            "query": query,
            "variables": variables
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Send the request
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        if response.status_code != 200:
            raise OxaigenApiException(message=f"Oxaigen Client API connection error: {str(response.text)}")

        response_data = response.json()

        if "data" not in response_data:
            raise KeyError("Unknown API response, invalid query or input arguments provided.")

        response_data_dict: Dict = response_data["data"]

        # TODO: TO FIX!
        auth_failure = False
        # for key, value in response_data_dict:
        #     # e.g. key == 'getS3AssetDownloadLink',
        #     # e.g. value == {'__typename': 'AssetNotFound', 'errorMessage': 'Asset with asset key ["xxx"] not found.'}
        #     try:
        #         if "__typename" in value:
        #             if value["__typename"] == "AuthenticationError":
        #                 auth_failure = True
        #                 break
        #     except KeyError:
        #         continue
        #
        # if auth_failure:
        #     raise OxaigenApiException(message=f"Oxaigen Client API authentication error: please login again!")

        return response_data_dict
    except Exception as e:
        raise OxaigenApiException(message=f"Could not perform API call, error: {str(e)}")
