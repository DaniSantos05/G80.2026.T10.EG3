"""MODULE: projects_json_store. Contains the ProjectsJsonStore class"""
from main.python.uc3m_consulting.storage.json_store_master import JsonStoreMaster
from main.python.uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE


class ProjectsJsonStore(JsonStoreMaster):
    """Singleton store for projects"""

    #siendo privado el atributo, evitamos conflictos con clases hijas.
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ProjectsJsonStore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__(PROJECTS_STORE_FILE)
