"""MODULE: documents_json_store. Contains the DocumentsJsonStore class"""
from main.python.uc3m_consulting.storage.json_store_master import JsonStoreMaster
from main.python.uc3m_consulting.enterprise_manager_config import TEST_DOCUMENTS_STORE_FILE


class DocumentsJsonStore(JsonStoreMaster):
    """Singleton store for documents"""

    __instance = None

    def __new__(cls):
        """Singleton implementation for DocumentsJsonStore"""
        if cls.__instance is None:
            cls.__instance = super(DocumentsJsonStore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__(TEST_DOCUMENTS_STORE_FILE)
