"""MODULE: json_store_master. Contains the JsonStoreMaster class"""
import json
from main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class JsonStoreMaster:
    """Parent class for JSON stores"""

    def __init__(self, file_store):
        self._data_list = []
        self._file_name = file_store

    def load_json_file(self):
        """Loads and returns the content of a JSON store"""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format") from ex
        return self._data_list

    def save_json_file(self):
        """Saves the content of the data list into a JSON store"""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file or file path") from ex

    def add_item(self, item):
        """Loads the store, adds an item and saves"""
        self.load_json_file()
        self._data_list.append(item)
        self.save_json_file()

    def find_item(self, item_to_find):
        """Raises exception if item already exists in the store"""
        self.load_json_file()
        if item_to_find in self._data_list:
            raise EnterpriseManagementException("Duplicated project in projects list")
