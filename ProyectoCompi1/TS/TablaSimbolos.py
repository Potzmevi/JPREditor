

from TS.Tipo import TIPO
from TS.Excepcion import Excepcion
from grammar import errores

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
        try:
            while tablaActual.tabla != None:
                if id in tablaActual.tabla :
                    return tablaActual.tabla[id]           # RETORNA SIMBOLO
                else:
                    tablaActual = tablaActual.anterior
            return None
        except:
            return Excepcion("Semantico", "Variable " +id + " No encontrada", 0, 0)

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id.lower() in tablaActual.tabla :
                if tablaActual.tabla[simbolo.id.lower()].getTipo() == simbolo.getTipo() or tablaActual.tabla[simbolo.id.lower()].getTipo()== TIPO.VAR or simbolo.getTipo()== TIPO.NULO or (simbolo.getTipo()==TIPO.DECIMAL and tablaActual.tabla[simbolo.id.lower()].getTipo()== TIPO.ENTERO):
                    if simbolo.getTipo()== TIPO.NULO:
                            tablaActual.tabla[simbolo.id.lower()].setValor(None)
                            tablaActual.tabla[simbolo.id.lower()].setTipo(TIPO.VAR)
                    else:
                        tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())
                        tablaActual.tabla[simbolo.id.lower()].setValor(simbolo.getValor())
                    return None             #VARIABLE ACTUALIZADA
                elif simbolo.getTipo() == 'INCREMENTO' or simbolo.getTipo() == 'DECREMENTO':
                    if (tablaActual.tabla[simbolo.id.lower()].getTipo() == TIPO.ENTERO or tablaActual.tabla[simbolo.id.lower()].getTipo() == TIPO.DECIMAL):
                        valorAnterior = tablaActual.tabla[simbolo.id.lower()].getValor()
                        tablaActual.tabla[simbolo.id.lower()].setValor(valorAnterior+simbolo.getValor())
                        return None
                return Excepcion("Semantico", "Tipo de dato Diferente en Asignacion", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())
        
    
