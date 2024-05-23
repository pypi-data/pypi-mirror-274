# -*- coding: utf-8 -*-
from .asset.asset import OxaigenAsset
from .authentication.authentication import OxaigenAuthentication
from .storage.data_storage import OxaigenDataStorage

class Oxaigen:
    """
    Oxaigen SDK Class
    """
    def __init__(self):
        self.auth = OxaigenAuthentication()
        self.asset = OxaigenAsset()
        self.storage = OxaigenDataStorage()

    def login(self) -> None:
        self.auth.login()

