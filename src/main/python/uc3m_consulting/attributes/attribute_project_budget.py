"""MODULE: attribute_project_budget. Contains the AttributeProjectBudget class"""
from main.python.uc3m_consulting.attributes.attribute import Attribute
from main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class AttributeProjectBudget(Attribute):
    """Definition of attribute ProjectBudget class"""

    def __init__(self, attr_value):
        """Definition of attribute ProjectBudget init method"""
        super().__init__()
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """Validates the project budget"""
        try:
            budget_float = float(attr_value)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        budget_text = str(budget_float)
        if '.' in budget_text:
            decimals = len(budget_text.split('.')[1])
            if decimals > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if budget_float < 50000 or budget_float > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")

        return attr_value