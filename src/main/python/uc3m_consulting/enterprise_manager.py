"""Module: enterprise_manager"""

import re
from datetime import datetime

from main.python.uc3m_consulting.enterprise_project import EnterpriseProject
from main.python.uc3m_consulting.enterprise_management_exception import (
    EnterpriseManagementException
)
from main.python.uc3m_consulting.project_document import ProjectDocument
from main.python.uc3m_consulting.num_docs_report import NumDocsReport

from main.python.uc3m_consulting.storage.projects_json_store import ProjectsJsonStore
from main.python.uc3m_consulting.storage.documents_json_store import DocumentsJsonStore
from main.python.uc3m_consulting.storage.num_docs_json_store import NumDocsJsonStore

from main.python.uc3m_consulting.enterprise_manager_config import (
    ERR_INVALID_DATE,
    ERR_WRONG_FILE,
    ERR_NO_DOCS,
    ERR_INCONSISTENT_SIGNATURE,
    KEY_REGISTER_DATE
)


class EnterpriseManager:
    """Singleton class for managing the orders"""

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(EnterpriseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    # pylint: disable=too-many-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         date: str,
                         budget: str):
        """Registers a new project"""

        new_project = EnterpriseProject(
            company_cif=company_cif,
            project_acronym=project_acronym,
            project_description=project_description,
            department=department,
            starting_date=date,
            project_budget=budget
        )

        store = ProjectsJsonStore()

        # comprueba duplicados (internamente lanza excepcion si existe)
        store.find_item(new_project.to_json())

        # añade el proyecto
        store.add_item(new_project.to_json())

        return new_project.project_id

    def find_docs(self, date_str):
        """Generates a JSON report counting valid documents for a specific date"""

        pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        if not pattern.fullmatch(date_str):
            raise EnterpriseManagementException(ERR_INVALID_DATE)

        try:
            datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException(ERR_INVALID_DATE) from ex

        documents_store = DocumentsJsonStore()
        documents = documents_store.load_json_file()

        if not documents:
            raise EnterpriseManagementException(ERR_WRONG_FILE)

        count = 0

        for doc in documents:
            # Usando la constante para la key
            timestamp = doc[KEY_REGISTER_DATE]
            doc_date = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")

            if doc_date == date_str:
                # Usando el classmethod del refactoring anterior
                if ProjectDocument.is_valid_document(doc):
                    count += 1
                else:
                    raise EnterpriseManagementException(ERR_INCONSISTENT_SIGNATURE)

        if count == 0:
            raise EnterpriseManagementException(ERR_NO_DOCS)

        # Usando la nueva clase de modelo para generar el informe
        report = NumDocsReport(query_date=date_str, num_files=count)

        num_docs_store = NumDocsJsonStore()
        num_docs_store.add_item(report.to_json())

        return count
