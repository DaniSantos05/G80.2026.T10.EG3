"""MODULE: attribute_project_description. Contains the AttributeProjectDescription class"""
from main.python.uc3m_consulting.attributes.attribute import Attribute


class AttributeProjectDescription(Attribute):
    """Definition of attribute ProjectDescription class"""

    def __init__(self, attr_value):
        """Definition of attribute ProjectDescription init method"""
        super().__init__()
        self._validation_pattern = r"^.{10,30}$"
        self._error_message = "Invalid description format"
        self._attr_value = self._validate(attr_value)
