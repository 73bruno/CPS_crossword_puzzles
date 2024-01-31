#########################################################################  
# Clase Variable
#########################################################################
class Variable:
    def __init__(self, row, col, direction, length, domain):
        self.row = row  # Fila en la que comienza la palabra
        self.col = col  # Columna en la que comienza la palabra
        self.direction = direction  # Dirección de la palabra ('horizontal' o 'vertical')
        self.length = length  # Longitud de la palabra
        self.domain = domain  # Objeto Dominio que contiene palabras válidas para esta variable
        self.value = None  # Valor asignado (letra o palabra)

    def assign(self, value):
        self.value = value

    def unassign(self):
        self.value = None

    def is_assigned(self):
        return self.value is not None

    def __str__(self):
        return f"Variable({self.row}, {self.col}, {self.direction}, {self.length}, domain={self.domain}, value={self.value})"