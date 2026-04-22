"""Module: enterprise_manager"""

import re
from datetime import datetime, timezone

from main.python.uc3m_consulting.enterprise_project import EnterpriseProject
from main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from main.python.uc3m_consulting.project_document import ProjectDocument

from main.python.uc3m_consulting.storage.projects_json_store import ProjectsJsonStore
from main.python.uc3m_consulting.storage.documents_json_store import DocumentsJsonStore
from main.python.uc3m_consulting.storage.num_docs_json_store import NumDocsJsonStore


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""

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

        # comprueba duplicados
        store.find_item(new_project.to_json())

        # añade el proyecto
        store.add_item(new_project.to_json())

        return new_project.project_id

    def find_docs(self, date_str):
        """Generates a JSON report counting valid documents for a specific date"""

        pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        if not pattern.fullmatch(date_str):
            raise EnterpriseManagementException("Invalid date format")

        try:
            datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        documents_store = DocumentsJsonStore()
        documents = documents_store.load_json_file()

        if not documents:
            raise EnterpriseManagementException("Wrong file or file path")

        count = 0

        for doc in documents:
            timestamp = doc["register_date"]
            doc_date = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")

            if doc_date == date_str:
                if ProjectDocument.is_valid_document(doc):
                    count += 1
                else:
                    raise EnterpriseManagementException(
                        "Inconsistent document signature"
                    )

        if count == 0:
            raise EnterpriseManagementException("No documents found")

        report = {
            "Querydate": date_str,
            "ReportDate": datetime.now(timezone.utc).timestamp(),
            "Numfiles": count
        }

        num_docs_store = NumDocsJsonStore()
        num_docs_store.add_item(report)

        return count
