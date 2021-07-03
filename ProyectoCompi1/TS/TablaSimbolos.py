from TS.Simbolo import Simbolo
from TS.Tipo import TIPO
from TS.Excepcion import Excepcion

simbolos=[]
entorno=""


def actualizarSimbolo(id,valor,tipo,fila,columna):
    global simbolos
    global entorno
    for simbolo in simbolos :
        if simbolo.id==id and simbolo.entorno==entorno and simbolo.fila==fila and simbolo.columna==columna :
            simbolo.setValor(valor)
            simbolo.setTipo(tipo)
            break

class TablaSimbolos:

    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior
    
    def setTabla(self, simbolo):      # Agregar una variable
        global simbolos
        global entorno
        if simbolo.id.lower() in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            bandera=True
            if len(simbolos)>0:
                for simboloo in simbolos:
                    if simboloo.id==simbolo.id and simboloo.entorno==entorno and simboloo.fila==simbolo.fila and simboloo.columna==simbolo.columna :
                        bandera=True
                        break
                    else:
                        bandera=False
                if bandera==False:
                    simbolo.entorno=entorno
                    simbolos.append(simbolo)
            else:
                simbolo.entorno=entorno
                simbolos.append(simbolo)
            return None

    def getSimbolos(self):
        return simbolos
    
    def vaciarSimbolos(self):
        global simbolos
        simbolos=[]
        
    def setEntorno(self, ambito):
        global entorno
        entorno= ambito
    
    def getTabla(self, id):            # obtener una variable
        tablaActual = self
        try:
            while tablaActual != None:
                if id.lower() in tablaActual.tabla :
                    return tablaActual.tabla[id.lower()]           # RETORNA SIMBOLO
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
                            actualizarSimbolo(simbolo.id,None,TIPO.VAR,simbolo.fila,simbolo.columna)
                    else:
                        tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())
                        tablaActual.tabla[simbolo.id.lower()].setValor(simbolo.getValor())
                        actualizarSimbolo(simbolo.id,simbolo.getValor(),simbolo.getTipo(),simbolo.fila,simbolo.columna)
                    return None             #VARIABLE ACTUALIZADA
                elif simbolo.getTipo() == 'INCREMENTO' or simbolo.getTipo() == 'DECREMENTO':
                    if (tablaActual.tabla[simbolo.id.lower()].getTipo() == TIPO.ENTERO or tablaActual.tabla[simbolo.id.lower()].getTipo() == TIPO.DECIMAL):
                        valorAnterior = tablaActual.tabla[simbolo.id.lower()].getValor()
                        tablaActual.tabla[simbolo.id.lower()].setValor(valorAnterior+simbolo.getValor())
                        actualizarSimbolo(simbolo.id,valorAnterior+simbolo.getValor(),tablaActual.tabla[simbolo.id.lower()].getTipo(),simbolo.fila,simbolo.columna)
                        return None
                return Excepcion("Semantico", "Tipo de dato Diferente en Asignacion", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())
        
    
    