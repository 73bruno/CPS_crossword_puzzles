# Un objeto de esta clase está formado por un número (tamaño) y
# una lista de palabras que tienen un número de caracteres igual al tamaño
class Dominio:
    def __init__(self, tam):
        self.tam=tam
        self.lista=[]
        self.podado=[]#lsita de listas
            
    def addPal(self, pal):
        self.lista.append(pal)
        
    def removePal(self, pal):
        self.lista.remove(pal)
        
    def getTam(self):
        return self.tam
    
    def getLista(self):
        return self.lista
    
    def contienePalabra(self, pal):
        return pal in self.lista
    
    def __str__(self):
        return f"Dominio (Tamaño: {self.tam}, Lista: {self.lista}, Podado: {self.podado})"


