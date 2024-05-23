# -*- coding: utf-8 -*-
from typing import Optional, Any

from .logging import logger


class OxaigenException(Exception):
    """
    Raise when an Oxaigen error is thrown
    """

    def __init__(self, message, *args):
        self.message = message
        logger.error(message)
        super().__init__(message, *args)


class OxaigenSDKException(OxaigenException):
    """
    Raised when an Oxaigen SDk error occurs.
    """

    def __init__(self, message, error: Optional[Any], *args):
        log_message = f"Exception occurred: {message}. SDK Error: {str(error)}"
        logger.debug(log_message)
        super().__init__(message, *args)


class OxaigenApiException(OxaigenException):
    """
    Raised when an API related error occurs.
    """

    def __init__(self, message, error: Optional[Any], *args):
        log_message = f"Exception occurred: {message}. API Error: {str(error)}"
        logger.debug(log_message)
        super().__init__(message, *args)
