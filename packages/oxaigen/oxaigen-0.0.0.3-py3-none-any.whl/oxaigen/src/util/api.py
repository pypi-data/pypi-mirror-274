# -*- coding: utf-8 -*-
import os
import requests
from typing import Dict, Any

from ..constant import ACCESS_TOKEN
from ..config import API_ENDPOINT
from .exception import OxaigenApiException
from .token import refresh_tokens


def run_api_query(query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    """
    Util function to call the Oxaigen Private Client API and handles authorization errors
    """
    try:
        access_token = os.environ.get(ACCESS_TOKEN)
        if not access_token:
            refresh_tokens()
            access_token = os.environ.get(ACCESS_TOKEN)

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

        auth_failure = False
        for item in response_data["data"]:
            try:
                if item["__typename"] == "AuthenticationError":
                    auth_failure = True
                    break
            except KeyError:
                continue

        if auth_failure:
            refresh_tokens()
            new_access_token = os.environ.get(ACCESS_TOKEN)
            new_headers = {
                "Authorization": f"Bearer {new_access_token}"
            }
            # re-send the request
            response = requests.post(API_ENDPOINT, json=payload, headers=new_headers)
            if response.status_code != 200:
                raise OxaigenApiException(message=f"Oxaigen Client API connection error: {str(response.text)}")

        return response_data["data"]
    except Exception:
        raise OxaigenApiException(message='Invalid login input, try again!')


