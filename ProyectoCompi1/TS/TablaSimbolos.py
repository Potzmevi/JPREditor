

from TS.Tipo import TIPO
from TS.Excepcion import Excepcion


class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior

    def setTabla(self, simbolo):      # Agregar una variable
        if simbolo.id.lower() in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            return None

    def getTabla(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual.tabla != None:
            if id in tablaActual.tabla :
                return tablaActual.tabla[id]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla :
                if tablaActual.tabla[simbolo.id].getTipo() == simbolo.getTipo() or tablaActual.tabla[simbolo.id].getTipo()== TIPO.VAR or simbolo.getTipo()== TIPO.NULO or (simbolo.getTipo()==TIPO.DECIMAL and tablaActual.tabla[simbolo.id].getTipo()== TIPO.ENTERO):
                    if simbolo.getTipo()== TIPO.NULO:
                            tablaActual.tabla[simbolo.id].setValor(None)
                            tablaActual.tabla[simbolo.id].setTipo(TIPO.VAR)
                    else:
                        tablaActual.tabla[simbolo.id].setTipo(simbolo.getTipo())
                        tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())
                    return None             #VARIABLE ACTUALIZADA
                elif simbolo.getTipo() == 'INCREMENTO' or simbolo.getTipo() == 'DECREMENTO':
                    if (tablaActual.tabla[simbolo.id].getTipo() == TIPO.ENTERO or tablaActual.tabla[simbolo.id].getTipo() == TIPO.DECIMAL):
                        print("entra")
                        valorAnterior = tablaActual.tabla[simbolo.id].getValor()
                        tablaActual.tabla[simbolo.id].setValor(valorAnterior+simbolo.getValor())
                        return None
                return Excepcion("Semantico", "Tipo de dato Diferente en Asignacion", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())
        
    
