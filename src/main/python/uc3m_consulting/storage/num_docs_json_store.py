"""MODULE: num_docs_json_store. Contains the NumDocsJsonStore class"""
from main.python.uc3m_consulting.storage.json_store_master import JsonStoreMaster
from main.python.uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE


class NumDocsJsonStore(JsonStoreMaster):
    """Store for num docs reports"""

    def __init__(self):
        super().__init__(TEST_NUMDOCS_STORE_FILE)
