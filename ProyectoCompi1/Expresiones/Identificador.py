from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST


class Identificador(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        try:
            simbolo = table.getTabla(self.identificador.lower())

            if simbolo == None:
                return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)

            self.tipo = simbolo.getTipo()
            
            return simbolo.getValor()
        except:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
    def getNodo(self):
        nodo = NodoAST("IDENTIFICADOR")
        nodo.agregarHijo(str(self.identificador))
        return nodo 