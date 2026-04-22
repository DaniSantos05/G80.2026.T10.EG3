"""MODULE: enterprise_project. Contains the EnterpriseProject class"""
import hashlib
import json
from datetime import datetime, timezone
import re
from main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from main.python.uc3m_consulting.attributes.attribute_project_acronym import AttributeProjectAcronym
from main.python.uc3m_consulting.attributes.attribute_cif import AttributeCIF
from main.python.uc3m_consulting.attributes.attribute_project_description import AttributeProjectDescription

class EnterpriseProject:
    """Class representing a project"""
    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self,
                 company_cif: str,
                 project_acronym: str,
                 project_description: str,
                 department: str,
                 starting_date: str,
                 project_budget: float):
        self.__company_cif = AttributeCIF(company_cif).value
        self.__project_description = AttributeProjectDescription(project_description).value
        self.__project_achronym = AttributeProjectAcronym(project_acronym).value
        self.__department = self.validate_department(department)
        self.__starting_date = self.validate_starting_date(starting_date)
        self.__project_budget = self.validate_project_budget(project_budget)
        justnow = datetime.now(timezone.utc)
        self.__time_stamp = datetime.timestamp(justnow)

    @staticmethod
    def validate_cif(cif: str):
        """validates a cif number """
        if not isinstance(cif, str):
            raise EnterpriseManagementException("CIF code must be a string")
        patron_cif = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not patron_cif.fullmatch(cif):
            raise EnterpriseManagementException("Invalid CIF format")

        primera_letra = cif[0]
        digitos = cif[1:8]
        caracter_control = cif[8]

        suma_pares_doblados = 0
        suma_impares = 0

        for i in range(len(digitos)):
            if i % 2 == 0:
                digito_doblado = int(digitos[i]) * 2
                if digito_doblado > 9:
                    suma_pares_doblados = suma_pares_doblados + (digito_doblado // 10) + (digito_doblado % 10)
                else:
                    suma_pares_doblados = suma_pares_doblados + digito_doblado
            else:
                suma_impares = suma_impares + int(digitos[i])

        suma_total = suma_pares_doblados + suma_impares
        ultimo_digito = suma_total % 10
        digito_control = 10 - ultimo_digito

        if digito_control == 10:
            digito_control = 0

        letras_control = "JABCDEFGHI"

        if primera_letra in ('A', 'B', 'E', 'H'):
            if str(digito_control) != caracter_control:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif primera_letra in ('P', 'Q', 'S', 'K'):
            if letras_control[digito_control] != caracter_control:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return cif

    @staticmethod
    def validate_project_acronym(project_acronym: str):
        """Validates the project acronym."""
        patron_acronimo = re.compile(r"^[a-zA-Z0-9]{5,10}")
        resultado = patron_acronimo.fullmatch(project_acronym)
        if not resultado:
            raise EnterpriseManagementException("Invalid acronym")
        return project_acronym

    @staticmethod
    def validate_starting_date(t_d):
        """validates the  date format  using regex"""
        mr = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        res = mr.fullmatch(t_d)
        if not res:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(t_d, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")

        return t_d

    @staticmethod
    def validate_project_description(project_description: str):
        """Validates the project description."""
        patron_descripcion = re.compile(r"^.{10,30}$")
        resultado = patron_descripcion.fullmatch(project_description)
        if not resultado:
            raise EnterpriseManagementException("Invalid description format")
        return project_description

    @staticmethod
    def validate_department(department: str):
        """Validates the department."""
        patron_departamento = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        resultado = patron_departamento.fullmatch(department)
        if not resultado:
            raise EnterpriseManagementException("Invalid department")
        return department

    @staticmethod
    def validate_project_budget(project_budget):
        """Validates the project budget."""
        try:
            presupuesto_float = float(project_budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        presupuesto_texto = str(presupuesto_float)
        if '.' in presupuesto_texto:
            decimales = len(presupuesto_texto.split('.')[1])
            if decimales > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if presupuesto_float < 50000 or presupuesto_float > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")

        return project_budget

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
        """Property representing the type of transfer: REGULAR, INMEDIATE or URGENT """
        return self.__project_achronym
    @project_acronym.setter
    def project_acronym(self, value):
        self.__project_achronym = value

    @property
    def project_budget(self):
        """Property respresenting the transfer amount"""
        return self.__project_budget
    @project_budget.setter
    def project_budget(self, value):
        self.__project_budget = value

    @property
    def department(self):
        """Property representing the transfer concept"""
        return self.__department
    @department.setter
    def department(self, value):
        self.__department = value

    @property
    def starting_date( self ):
        """Property representing the transfer's date"""
        return self.__starting_date
    @starting_date.setter
    def starting_date( self, value ):
        self.__starting_date = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def project_id(self):
        """Returns the md5 signature (transfer code)"""
        return hashlib.md5(str(self).encode()).hexdigest()
