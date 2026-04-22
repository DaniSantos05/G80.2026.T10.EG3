"""MODULE: attribute_cif. Contains the AttributeCIF class"""
from main.python.uc3m_consulting.attributes.attribute import Attribute
from main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class AttributeCIF(Attribute):
    """Definition of attribute CIF class"""

    def __init__(self, attr_value):
        """Definition of attribute CIF init method"""
        super().__init__()
        self._validation_pattern = r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$"
        self._error_message = "Invalid CIF format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """Validates CIF format and control character"""
        if not isinstance(attr_value, str):
            raise EnterpriseManagementException("CIF code must be a string")

        # valida el formato con el regex de la clase padre
        attr_value = super()._validate(attr_value)

        # lógica específica del dígito de control
        primera_letra = attr_value[0]
        digitos = attr_value[1:8]
        caracter_control = attr_value[8]

        suma_pares_doblados = 0
        suma_impares = 0

        for i in range(len(digitos)):
            if i % 2 == 0:
                digito_doblado = int(digitos[i]) * 2
                if digito_doblado > 9:
                    suma_pares_doblados += (digito_doblado // 10) + (digito_doblado % 10)
                else:
                    suma_pares_doblados += digito_doblado
            else:
                suma_impares += int(digitos[i])

        suma_total = suma_pares_doblados + suma_impares
        ultimo_digito = suma_total % 10
        digito_control = 10 - ultimo_digito

        if digito_control == 10:
            digito_control = 0

        letras_control = "JABCDEFGHI"

        if primera_letra in ('A', 'B', 'E', 'H'):
            if str(digito_control) != caracter_control:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif primera_letra in ('P', 'Q', 'S', 'K'):
            if letras_control[digito_control] != caracter_control:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")

        return attr_value
