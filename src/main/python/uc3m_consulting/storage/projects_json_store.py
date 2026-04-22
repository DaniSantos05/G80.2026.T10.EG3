"""MODULE: projects_json_store. Contains the ProjectsJsonStore class"""
from main.python.uc3m_consulting.storage.json_store_master import JsonStoreMaster
from main.python.uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE


class ProjectsJsonStore(JsonStoreMaster):
    """Store for projects"""

    def __init__(self):
        super().__init__(PROJECTS_STORE_FILE)
