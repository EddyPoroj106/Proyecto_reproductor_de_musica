class NodoCancion:
    def __init__(self, nombre, artista, duracion, ruta):
        self.nombre = nombre
        self.artista = artista
        self.duracion = duracion
        self.ruta = ruta
        self.siguiente = None
        self.anterior = None


class lista_de_reproduccion:
    def __init__(self):
        self.cabeza = None
        self.actual = None
        self.tamano = 0
    
    def esta_vacia(self):
        return self.cabeza is None
    
    def agregar_cancion(self, nombre, artista, duracion, ruta):
        nuevo_nodo = NodoCancion(nombre, artista, duracion, ruta)
        
        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
            self.actual = nuevo_nodo
        else:
            ultimo = self.cabeza.anterior
            
            nuevo_nodo.siguiente = self.cabeza
            nuevo_nodo.anterior = ultimo
            
            ultimo.siguiente = nuevo_nodo
            self.cabeza.anterior = nuevo_nodo
        
        self.tamano += 1
    
    