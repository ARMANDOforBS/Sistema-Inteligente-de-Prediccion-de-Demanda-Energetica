from abc import ABC, abstractmethod

class UsuarioEnergia(ABC):
    def __init__(self, nombre_tipo):
        self.nombre_tipo = nombre_tipo

    @abstractmethod
    def calcular_tarifa_base(self):
        pass

    @abstractmethod
    def perfil_consumo(self):
        pass

class UsuarioResidencial(UsuarioEnergia):
    def __init__(self):
        super().__init__("Residencial")

    def calcular_tarifa_base(self):
        # Tarifa subsidiada o estándar
        return 0.12  # $0.12 por kWh

    def perfil_consumo(self):
        return "Consumo moderado, picos en mañanas y noches."

class UsuarioComercial(UsuarioEnergia):
    def __init__(self):
        super().__init__("Comercial")

    def calcular_tarifa_base(self):
        # Tarifa comercial variable
        return 0.18  # $0.18 por kWh

    def perfil_consumo(self):
        return "Consumo alto en horario laboral."

class UsuarioIndustrial(UsuarioEnergia):
    def __init__(self):
        super().__init__("Industrial")

    def calcular_tarifa_base(self):
        # Tarifa industrial
        return 0.10  # $0.10 por kWh

    def perfil_consumo(self):
        return "Consumo muy alto y constante, maquinaria pesada."

def factory_usuario(tipo_str):
    """Factory method para crear instancias basadas en strings."""
    tipo_str = tipo_str.strip().capitalize()
    if tipo_str == "Residencial":
        return UsuarioResidencial()
    elif tipo_str == "Comercial":
        return UsuarioComercial()
    elif tipo_str == "Industrial":
        return UsuarioIndustrial()
    else:
        return UsuarioResidencial()
