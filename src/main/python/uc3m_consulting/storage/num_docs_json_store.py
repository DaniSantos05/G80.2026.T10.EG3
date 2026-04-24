"""MODULE: num_docs_json_store. Contains the NumDocsJsonStore class"""
from uc3m_consulting.storage.json_store_master import JsonStoreMaster
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE


class NumDocsJsonStore(JsonStoreMaster):
    """Singleton store for num docs reports"""

    __instance = None

    def __new__(cls):
        """Singleton implementation for NumDocsJsonStore"""
        if cls.__instance is None:
            cls.__instance = super(NumDocsJsonStore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__(TEST_NUMDOCS_STORE_FILE)
