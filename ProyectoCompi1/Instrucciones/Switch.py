from Abstract.Instruccion import Instruccion
from TS.Excepcion         import Excepcion
from TS.Tipo              import TIPO
from TS.Tipo              import OperadorRelacional
from TS.TablaSimbolos     import TablaSimbolos
from Expresiones.Relacional     import Relacional

class Switch(Instruccion):
    def __init__(self, expresion, lst_case,default, fila, columna):
        self.expresion         = expresion
        self.lst_case          = lst_case
        self.default       = default
        self.fila              = fila
        self.columna           = columna

    def interpretar(self, tree, table):
        if self.lst_case == None:
            if self.default != None:
                self.default.interpretar(tree,table)
        else:
            result = False
            for case in self.lst_case:
                value_case = case.expresion.interpretar(tree,table)
                if isinstance(value_case, Excepcion): return value_case

                value_expresion = self.expresion.interpretar(tree,table)
                if isinstance(value_expresion,Excepcion): return value_expresion

                if value_expresion == value_case:
                    result = case.interpretar(tree, table)
                    break
            if not(result): # si result  == true --> el caso evaluado trae break
                if self.default != None:
                    self.default.interpretar(tree,table)





    def instruccionesInterpreter(self, instruccion, tree, table):

    # REALIZAR LAS ACCIONES
        if isinstance(instruccion, list):           #agregado
            for element in instruccion:
                self.instruccionesInterpreter(element, tree,table)
        else:              
            value = instruccion.interpretar(tree,table)
            if isinstance(value, Excepcion) :
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())