# -*- coding: utf-8 -*-
import os
from typing import Optional

from .constant import (
    TOKEN_FILE_NAME,
    OXAIGEN_CONFIG_DIR,
)

CLIENT_SERVER_IP_ENV_VAR = "CLIENT_SERVER_IP"
CLIENT_SERVER_PORT_ENV_VAR = "CLIENT_SERVER_PORT"
ROOT_DIR_ENV_VAR = "ROOT_DIR"
JUPYTERHUB_ROOT_DIR_ENV_VAR = "JUPYTERHUB_ROOT_DIR"


def get_env_var_with_fallback(primary: str, fallback: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(primary) or os.getenv(fallback, default)


# General configuration
USER_ROOT_DIR = get_env_var_with_fallback(ROOT_DIR_ENV_VAR, JUPYTERHUB_ROOT_DIR_ENV_VAR)

# Authentication configuration
TOKEN_FILE_PATH = os.path.join(f"{USER_ROOT_DIR}/{OXAIGEN_CONFIG_DIR}", TOKEN_FILE_NAME)

# API configuration
API_ENDPOINT = f"http://{os.environ.get(CLIENT_SERVER_IP_ENV_VAR)}:{os.environ.get(CLIENT_SERVER_PORT_ENV_VAR)}/v1/graphql"

# Data Storage configuration
S3_ENDPOINT = get_env_var_with_fallback('S3_ENDPOINT', 'JUPYTERLAB_S3_ENDPOINT')
S3_ACCESS_KEY_ID = get_env_var_with_fallback('S3_ACCESS_KEY_ID', 'JUPYTERLAB_S3_ACCESS_KEY_ID')
S3_SECRET_ACCESS_KEY = get_env_var_with_fallback('S3_SECRET_ACCESS_KEY', 'JUPYTERLAB_S3_SECRET_ACCESS_KEY')
S3_SSL = get_env_var_with_fallback('S3_SSL', 'JUPYTERLAB_S3_SSL', 'True').lower() == 'true'
S3_REGION = get_env_var_with_fallback('S3_REGION', 'JUPYTERLAB_S3_REGION')
