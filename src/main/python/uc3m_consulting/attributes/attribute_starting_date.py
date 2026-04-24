"""MODULE: attribute_starting_date. Contains the AttributeStartingDate class"""
from datetime import datetime, timezone
from main.python.uc3m_consulting.attributes.attribute import Attribute
from main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class AttributeStartingDate(Attribute):
    """Definition of attribute StartingDate class"""

    def __init__(self, attr_value):
        """Definition of attribute StartingDate init method"""
        super().__init__()
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._error_message = "Invalid date format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """Validates the starting date format and value"""
        attr_value = super()._validate(attr_value)

        try:
            my_date = datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")

        return attr_value
