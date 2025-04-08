import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from pygame import mixer

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
    
    def siguiente_cancion(self):
        if not self.esta_vacia():
            self.actual = self.actual.siguiente
            return self.actual
        return None
    
    def cancion_anterior(self):
        if not self.esta_vacia():
            self.actual = self.actual.anterior
            return self.actual
        return None
    
    def obtener_cancion_actual(self):
        return self.actual


class ReproductorMusica:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor Musical")
        self.root.geometry("500x350")
        self.root.configure(bg='#f0f0f0')
        
        # Inicializar pygame mixer
        mixer.init()
        
        # Crear lista de reproducción
        self.lista_reproduccion = lista_de_reproduccion()
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')
        
        # Interfaz gráfica
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=15, pady=15)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Título
        titulo = ttk.Label(main_frame, text="---> REPRODUCTOR <---", font=('Arial', 14, 'bold'))
        titulo.pack(pady=(0, 10))
        
        # Lista de canciones
        self.lista_canciones = ttk.Treeview(
            main_frame, 
            columns=('Artista', 'Duración'), 
            selectmode='browse',
            height=8
        )
        self.lista_canciones.heading('#0', text='Canción')
        self.lista_canciones.heading('Artista', text='Artista')
        self.lista_canciones.heading('Duración', text='Duración')
        self.lista_canciones.column('#0', width=200, anchor='w')
        self.lista_canciones.column('Artista', width=150, anchor='w')
        self.lista_canciones.column('Duración', width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.lista_canciones.yview)
        self.lista_canciones.configure(yscrollcommand=scrollbar.set)
        
        self.lista_canciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de controles
        controles_frame = tk.Frame(main_frame, bg='#f0f0f0')
        controles_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Botones
        btn_frame = tk.Frame(controles_frame, bg='#f0f0f0')
        btn_frame.pack()
        
        btn_agregar = ttk.Button(btn_frame, text="Agregar", command=self.agregar_cancion)
        btn_agregar.grid(row=0, column=0, padx=5)
        
        btn_anterior = ttk.Button(btn_frame, text="⏮", width=3, command=self.cancion_anterior)
        btn_anterior.grid(row=0, column=1, padx=5)
        
        btn_reproducir = ttk.Button(btn_frame, text="▶", width=3, command=self.reproducir)
        btn_reproducir.grid(row=0, column=2, padx=5)
        
        btn_pausa = ttk.Button(btn_frame, text="⏸", width=3, command=self.pausar)
        btn_pausa.grid(row=0, column=3, padx=5)
        
        btn_siguiente = ttk.Button(btn_frame, text="⏭", width=3, command=self.siguiente_cancion)
        btn_siguiente.grid(row=0, column=4, padx=5)

    def agregar_cancion(self):
        archivos = filedialog.askopenfilenames(
            title="Seleccionar canciones",
            filetypes=(("Archivos MP3", "*.mp3"), ("Todos los archivos", "*.*")))
        
        for archivo in archivos:
            nombre = os.path.basename(archivo).split('.')[0]
            artista = "Desconocido"
            duracion = "0:00"
            
            self.lista_reproduccion.agregar_cancion(nombre, artista, duracion, archivo)
            self.lista_canciones.insert('', 'end', text=nombre, values=(artista, duracion))
    
    def reproducir(self):
        if not self.lista_reproduccion.esta_vacia():
            cancion_actual = self.lista_reproduccion.obtener_cancion_actual()
            mixer.music.load(cancion_actual.ruta)
            mixer.music.play()
    
    def pausar(self):
        if mixer.music.get_busy():
            mixer.music.pause()
        else:
            mixer.music.unpause()
    
    def siguiente_cancion(self):
        if not self.lista_reproduccion.esta_vacia():
            self.lista_reproduccion.siguiente_cancion()
            self.reproducir()
    
    def cancion_anterior(self):
        if not self.lista_reproduccion.esta_vacia():
            self.lista_reproduccion.cancion_anterior()
            self.reproducir()


if __name__ == "__main__":
    root = tk.Tk()
    app = ReproductorMusica(root)
    root.mainloop()



