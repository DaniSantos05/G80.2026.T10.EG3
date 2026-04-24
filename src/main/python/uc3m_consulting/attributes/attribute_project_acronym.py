"""MODULE: attribute_project_acronym. Contains the AttributeProjectAcronym class"""
from uc3m_consulting.attributes.attribute import Attribute


class AttributeProjectAcronym(Attribute):
    """Definition of attribute ProjectAcronym class"""

    def __init__(self, attr_value):
        """Definition of attribute ProjectAcronym init method"""
        super().__init__()
        self._validation_pattern = r"^[a-zA-Z0-9]{5,10}$"
        self._error_message = "Invalid acronym"
        self._attr_value = self._validate(attr_value)
