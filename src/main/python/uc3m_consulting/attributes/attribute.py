"""MODULE: attribute. Contains the Attribute class"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class Attribute:
    """Attribute class definition"""

    def __init__(self):
        self._validation_pattern = r""
        self._error_message = ""
        self._attr_value = ""

    def _validate(self, attr_value):
        """Attribute validation definition"""
        my_regex = re.compile(self._validation_pattern)
        regex_matches = my_regex.fullmatch(attr_value)
        if not regex_matches:
            raise EnterpriseManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        """Returns attr_value"""
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        """Sets attr_value"""
        self._attr_value = self._validate(attr_value)
