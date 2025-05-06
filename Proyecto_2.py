import tkinter as tk
from tkinter import ttk, filedialog
from pygame import mixer
import os


class Nodo_cancion:
    def __init__(self, nombre, ruta):
        self.nombre = nombre
        self.ruta = ruta
        self.anterior = None
        self.siguiente = None


class lista_de_reproduccion:
    def __init__(self):
        self.cabeza = None
        self.actual = None
        self.tamano = 0

    def esta_vacia(self):
        return self.cabeza is None

    def agregar_cancion(self, nombre, ruta):
        nueva = Nodo_cancion(nombre, ruta)
        if self.esta_vacia():
            self.cabeza = nueva
            nueva.siguiente = nueva
            nueva.anterior = nueva
        else:
            cola = self.cabeza.anterior
            cola.siguiente = nueva
            nueva.anterior = cola
            nueva.siguiente = self.cabeza
            self.cabeza.anterior = nueva
        self.actual = nueva
        self.tamano += 1

    def avanzar(self):
        if not self.esta_vacia():
            self.actual = self.actual.siguiente

    def retroceder(self):
        if not self.esta_vacia():
            self.actual = self.actual.anterior

    def obtener_cancion_actual(self):
        return self.actual

    def eliminar_cancion_actual(self):
        if self.esta_vacia():
            return

        if self.tamano == 1:
            self.cabeza = None
            self.actual = None
        else:
            anterior = self.actual.anterior
            siguiente = self.actual.siguiente
            anterior.siguiente = siguiente
            siguiente.anterior = anterior

            if self.actual == self.cabeza:
                self.cabeza = siguiente

            self.actual = siguiente

        self.tamano -= 1


class InterfazReproductor:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor MP3")
        self.root.geometry("650x400")
        self.root.configure(bg="white")

        mixer.init()
        self.lista_reproduccion = lista_de_reproduccion()

        self.lista_canciones = ttk.Treeview(self.root)
        self.lista_canciones["columns"] = ("Nombre",)
        self.lista_canciones.column("#0", width=0, stretch=tk.NO)
        self.lista_canciones.column("Nombre", anchor=tk.W, width=600)
        self.lista_canciones.heading("Nombre", text="Nombre", anchor=tk.W)
        self.lista_canciones.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack()

        ttk.Button(btn_frame, text="Agregar Canción", command=self.agregar_cancion).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="⏮", width=3, command=self.retroceder).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="▶", width=3, command=self.reproducir).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="⏸", width=3, command=self.pausar).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="⏹", width=3, command=self.detener).grid(row=0, column=4, padx=5)
        ttk.Button(btn_frame, text="⏭", width=3, command=self.avanzar).grid(row=0, column=5, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_cancion).grid(row=0, column=6, padx=5)

        self.cancion_actual_label = ttk.Label(self.root, text="", background="white", font=("Helvetica", 10))
        self.cancion_actual_label.pack(pady=10)

    def agregar_cancion(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos MP3", "*.mp3")])
        if ruta:
            nombre = os.path.basename(ruta)
            self.lista_reproduccion.agregar_cancion(nombre, ruta)
            self.lista_canciones.insert("", "end", text=nombre, values=(nombre,))

    def reproducir(self):
        if not self.lista_reproduccion.esta_vacia():
            cancion = self.lista_reproduccion.obtener_cancion_actual()
            if not mixer.music.get_busy():
                mixer.music.load(cancion.ruta)
                mixer.music.play()
            else:
                mixer.music.unpause()
            self.cancion_actual_label.config(text="Reproduciendo: " + cancion.nombre)

    def pausar(self):
        mixer.music.pause()
        self.cancion_actual_label.config(text="Pausado")

    def detener(self):
        mixer.music.stop()
        self.cancion_actual_label.config(text="Detenido")

    def avanzar(self):
        self.lista_reproduccion.avanzar()
        self.reproducir()

    def retroceder(self):
        self.lista_reproduccion.retroceder()
        self.reproducir()

    def eliminar_cancion(self):
        if not self.lista_reproduccion.esta_vacia():
            cancion_actual = self.lista_reproduccion.obtener_cancion_actual()
            nombre = cancion_actual.nombre

            for item in self.lista_canciones.get_children():
                if self.lista_canciones.item(item, 'values')[0] == nombre:
                    self.lista_canciones.delete(item)
                    break

            self.lista_reproduccion.eliminar_cancion_actual()
            mixer.music.stop()
            self.cancion_actual_label.config(text="Canción eliminada")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazReproductor(root)
    root.mainloop()
