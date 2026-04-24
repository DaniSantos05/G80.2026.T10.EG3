"""class for testing the find_docs method"""
import unittest
import json
import os.path
import hashlib
from unittest import TestCase
from os import remove
from datetime import datetime, timezone
from freezegun import freeze_time

# Importamos las constantes necesarias
from main.python.uc3m_consulting.enterprise_manager_config import (
    TEST_NUMDOCS_STORE_FILE, ERR_INVALID_DATE, ERR_NO_DOCS, ERR_WRONG_FILE
)
from main.python.uc3m_consulting.enterprise_manager import EnterpriseManager
from main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

from main.python.uc3m_consulting.storage.projects_json_store import ProjectsJsonStore
from main.python.uc3m_consulting.storage.documents_json_store import DocumentsJsonStore
from main.python.uc3m_consulting.storage.num_docs_json_store import NumDocsJsonStore


class TestFindDocsMethod(TestCase):
    """Class for testing find_docs method"""

    def setUp(self):
        """inicializo el entorno de prueba y reseteo Singletons"""
        EnterpriseManager._instance = None
        ProjectsJsonStore._instance = None
        DocumentsJsonStore._instance = None
        NumDocsJsonStore._instance = None

        if os.path.exists(TEST_NUMDOCS_STORE_FILE):
            remove(TEST_NUMDOCS_STORE_FILE)

    @staticmethod
    def read_file():
        """ this method read a Json file and return the value """
        my_file = TEST_NUMDOCS_STORE_FILE
        try:
            with open(my_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException(ERR_WRONG_FILE) from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    # pylint: disable=too-many-locals
    @freeze_time("2026/12/31 13:00:00")
    def test_valid_date(self):
        """validates a valid case with a valid date finding documents
        and updating the numdocs_store.json file"""
        mngr = EnterpriseManager()
        res = mngr.find_docs("05/04/2026")
        self.assertEqual(2, res)
        data = self.read_file()
        data_found = False
        for report in data:
            if (report["Querydate"] == "05/04/2026" and
                    report["ReportDate"] == datetime.now(timezone.utc).timestamp() and
                    report["Numfiles"] == 2):
                data_found = True
        self.assertTrue(data_found)

    @freeze_time("2026/12/31 13:00:00")
    def test_file_wrong_date(self):
        """path with wrong date format (exception)"""
        mngr = EnterpriseManager()

        if os.path.isfile(TEST_NUMDOCS_STORE_FILE):
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(EnterpriseManagementException) as cm_obj:
            mngr.find_docs("/04/2026")
        # Usamos la constante aquí
        self.assertEqual(ERR_INVALID_DATE, cm_obj.exception.message)

        if os.path.isfile(TEST_NUMDOCS_STORE_FILE):
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    @freeze_time("2026/12/31 13:00:00")
    def test_report_not_found(self):
        """path with no documents found (exception)"""
        mngr = EnterpriseManager()

        if os.path.isfile(TEST_NUMDOCS_STORE_FILE):
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(EnterpriseManagementException) as cm_obj:
            mngr.find_docs("01/04/2025")
        # Usamos la constante aquí
        self.assertEqual(ERR_NO_DOCS, cm_obj.exception.message)

        if os.path.isfile(TEST_NUMDOCS_STORE_FILE):
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)


if __name__ == '__main__':
    unittest.main()
