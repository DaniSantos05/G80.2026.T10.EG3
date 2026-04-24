"""MODULE: enterprise_project. Contains the EnterpriseProject class"""
import hashlib
import json
from datetime import datetime, timezone

# Fíjate que ya no necesitamos importar 're' ni 'EnterpriseManagementException' aquí,
# porque de eso ya se encargan las clases Attribute.

from main.python.uc3m_consulting.attributes.attribute_project_acronym import AttributeProjectAcronym
from main.python.uc3m_consulting.attributes.attribute_cif import AttributeCIF
from main.python.uc3m_consulting.attributes.attribute_project_description import AttributeProjectDescription
from main.python.uc3m_consulting.attributes.attribute_department import AttributeDepartment
from main.python.uc3m_consulting.attributes.attribute_starting_date import AttributeStartingDate
from main.python.uc3m_consulting.attributes.attribute_project_budget import AttributeProjectBudget


class EnterpriseProject:
    """Class representing a project"""

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self,
                 company_cif: str,
                 project_acronym: str,
                 project_description: str,
                 department: str,
                 starting_date: str,
                 project_budget: float):
        # Delegamos toda la validación a las clases especialistas
        self.__company_cif = AttributeCIF(company_cif).value
        self.__project_description = AttributeProjectDescription(project_description).value
        self.__project_achronym = AttributeProjectAcronym(project_acronym).value
        self.__department = AttributeDepartment(department).value
        self.__starting_date = AttributeStartingDate(starting_date).value
        self.__project_budget = AttributeProjectBudget(project_budget).value

        justnow = datetime.now(timezone.utc)
        self.__time_stamp = datetime.timestamp(justnow)

    def __str__(self):
        return "Project:" + json.dumps(self.__dict__)

    def to_json(self):
        """returns the object information in json format"""
        return {
            "company_cif": self.__company_cif,
            "project_description": self.__project_description,
            "project_acronym": self.__project_achronym,
            "project_budget": self.__project_budget,
            "department": self.__department,
            "starting_date": self.__starting_date,
            "time_stamp": self.__time_stamp,
            "project_id": self.project_id
        }

    @property
    def company_cif(self):
        """Company's cif"""
        return self.__company_cif

    @company_cif.setter
    def company_cif(self, value):
        self.__company_cif = value

    @property
    def project_description(self):
        """Project description"""
        return self.__project_description

    @project_description.setter
    def project_description(self, value):
        self.__project_description = value

    @property
    def project_acronym(self):
        """Property representing the project acronym"""
        return self.__project_achronym

    @project_acronym.setter
    def project_acronym(self, value):
        self.__project_achronym = value

    @property
    def project_budget(self):
        """Property representing the project budget"""
        return self.__project_budget

    @project_budget.setter
    def project_budget(self, value):
        self.__project_budget = value

    @property
    def department(self):
        """Property representing the department"""
        return self.__department

    @department.setter
    def department(self, value):
        self.__department = value

    @property
    def starting_date(self):
        """Property representing the transfer's date"""
        return self.__starting_date

    @starting_date.setter
    def starting_date(self, value):
        self.__starting_date = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def project_id(self):
        """Returns the md5 signature"""
        return hashlib.md5(str(self).encode()).hexdigest()
