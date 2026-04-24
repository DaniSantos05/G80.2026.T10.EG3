"""Module containing the NumDocsReport class"""
from datetime import datetime, timezone


class NumDocsReport:
    """Class representing a document search report"""

    def __init__(self, query_date: str, num_files: int):
        self.__query_date = query_date
        self.__num_files = num_files
        self.__report_date = datetime.now(timezone.utc).timestamp()

    def to_json(self):
        """Returns the object information in JSON format"""
        return {
            "Querydate": self.__query_date,
            "ReportDate": self.__report_date,
            "Numfiles": self.__num_files
        }
