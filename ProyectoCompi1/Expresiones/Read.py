from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Tipo import TIPO
from tkinter import messagebox
import tkinter as tk

class Read(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.CADENA

    def messageBox(self,prompt):
        root = tk.Toplevel()
        var = tk.StringVar()
        # GUI
        label = tk.Label(root, text=prompt)
        entry = tk.Entry(root, textvariable=var)
        label.pack(side="left", padx=(20, 0), pady=20)
        entry.pack(side="right", fill="x", padx=(0, 20), pady=20, expand=True)
        # Se detruye el formulario cuando se presiona enter
        entry.bind("<Return>", lambda event: root.destroy())
        # Espera hasta que la ventana se destruya
        root.wait_window()
        # Despues de que la ventana se destruye accedemos a ella
        value = var.get()
        return value
         
    def interpretar(self, tree, table):
        lectura = self.messageBox("Ingrese el valor del read") 
        return lectura

    def getNodo(self):
        nodo = NodoAST("READ")
        return nodo
    