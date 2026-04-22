"""MODULE: documents_json_store. Contains the DocumentsJsonStore class"""
from main.python.uc3m_consulting.storage.json_store_master import JsonStoreMaster
from main.python.uc3m_consulting.enterprise_manager_config import TEST_DOCUMENTS_STORE_FILE


class DocumentsJsonStore(JsonStoreMaster):
    """Store for documents"""

    def __init__(self):
        super().__init__(TEST_DOCUMENTS_STORE_FILE)
