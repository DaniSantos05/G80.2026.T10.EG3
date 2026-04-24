"""MODULE: jsonn_store. Contains the JsonStore class"""
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class JsonStore:
    """Class for managing JSON stores"""

    @staticmethod
    def load_json_store(file_path):
        """Loads and returns the content of a JSON store"""
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                lista_elementos = json.load(file)
        except FileNotFoundError:
            lista_elementos = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format"
            ) from ex

        return lista_elementos

    @staticmethod
    def save_json_store(file_path, data_list):
        """Saves the content of a list into a JSON store."""
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format"
            ) from ex