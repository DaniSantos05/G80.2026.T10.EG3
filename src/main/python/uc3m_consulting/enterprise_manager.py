"""Module """
import re
import json

from datetime import datetime, timezone
from freezegun import freeze_time
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.json_store import JsonStore


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def _cargar_proyectos_del_almacen(self):
        """Carga la lista de proyectos almacenados en JSON."""
        return JsonStore.load_json_store(PROJECTS_STORE_FILE)

    def _guardar_proyectos_en_almacen(self, lista_proyectos):
        """Guarda la lista de proyectos en el almacén JSON."""
        JsonStore.save_json_store(PROJECTS_STORE_FILE, lista_proyectos)

    #pylint: disable=too-many-arguments, too-many-positional-arguments
    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         date: str,
                         budget: str):
        """registers a new project"""
        patron_descripcion = re.compile(r"^.{10,30}$")
        resultado = patron_descripcion.fullmatch(project_description)
        if not resultado:
            raise EnterpriseManagementException("Invalid description format")

        patron_departamento = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        resultado = patron_departamento.fullmatch(department)
        if not resultado:
            raise EnterpriseManagementException("Invalid department")

        try:
            presupuesto_float = float(budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        presupuesto_texto = str(presupuesto_float)
        if '.' in presupuesto_texto:
            decimales = len(presupuesto_texto.split('.')[1])
            if decimales > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if presupuesto_float < 50000 or presupuesto_float > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")

        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        lista_proyectos = self._cargar_proyectos_del_almacen()

        for proyecto_almacenado in lista_proyectos:
            if proyecto_almacenado == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

        lista_proyectos.append(new_project.to_json())

        self._guardar_proyectos_en_almacen(lista_proyectos)

        return new_project.project_id



    def find_docs(self, date_str):
        """
        Generates a JSON report counting valid documents for a specific date.

        Checks cryptographic hashes and timestamps to ensure historical data integrity.
        Saves the output to 'resultado.json'.

        Args:
            date_str (str): date to query.

        Returns:
            number of documents found if report is successfully generated and saved.

        Raises:
            EnterpriseManagementException: On invalid date, file IO errors,
                missing data, or cryptographic integrity failure.
        """
        mr = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        res = mr.fullmatch(date_str)
        if not res:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex


        # open documents
        try:
            with open(TEST_DOCUMENTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                d_list = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex


        rst = 0

        # loop to find
        for el in d_list:
            time_val = el["register_date"]

            # string conversion for easy match
            doc_date_str = datetime.fromtimestamp(time_val).strftime("%d/%m/%Y")

            if doc_date_str == date_str:
                d_obj = datetime.fromtimestamp(time_val, tz=timezone.utc)
                with freeze_time(d_obj):
                    # check the project id (thanks to freezetime)
                    # if project_id are different then the data has been
                    #manipulated
                    p = ProjectDocument(el["project_id"], el["file_name"])
                    if p.document_signature == el["document_signature"]:
                        rst = rst + 1
                    else:
                        raise EnterpriseManagementException("Inconsistent document signature")

        if rst == 0:
            raise EnterpriseManagementException("No documents found")
        # prepare json text
        now_str = datetime.now(timezone.utc).timestamp()
        s = {"Querydate":  date_str,
             "ReportDate": now_str,
             "Numfiles": rst
             }

        try:
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                dl = json.load(file)
        except FileNotFoundError:
            dl = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        dl.append(s)
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(dl, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        return rst
