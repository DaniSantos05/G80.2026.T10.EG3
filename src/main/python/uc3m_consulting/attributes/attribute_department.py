"""MODULE: attribute_department. Contains the AttributeDepartment class"""
from main.python.uc3m_consulting.attributes.attribute import Attribute


class AttributeDepartment(Attribute):
    """Definition of attribute Department class"""

    def __init__(self, attr_value):
        """Definition of attribute Department init method"""
        super().__init__()
        self._validation_pattern = r"(HR|FINANCE|LEGAL|LOGISTICS)"
        self._error_message = "Invalid department"
        self._attr_value = self._validate(attr_value)
