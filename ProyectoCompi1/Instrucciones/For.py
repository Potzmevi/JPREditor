from Abstract.Instruccion import Instruccion
from Instrucciones.Break import Break
from TS.Excepcion         import Excepcion
from TS.Tipo              import TIPO
from TS.TablaSimbolos     import TablaSimbolos

class For(Instruccion):
    def __init__(self, valor, condicion, incremento, instrucciones,fila,columna):
        self.condicion         = condicion
        self.valor             = valor
        self.incremento        = incremento
        self.instrucciones     = instrucciones
        self.fila              = fila
        self.columna           = columna

        

    def interpretar(self, tree, table):
        valor = self.valor.interpretar(tree,table)
        if isinstance(valor, Excepcion): return valor

        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) == True:  # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL FOR
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                else:
                    break
            else:
                return Excepcion("Semantico", "Error en la expresion For ", self.fila, self.columna)
            self.incremento.interpretar(tree,table)


    def instruccionesInterpreter(self, instruccion, tree, table):

    # REALIZAR LAS ACCIONES
        if isinstance(instruccion, list):          
            for element in instruccion:
                self.instruccionesInterpreter(element, tree,table)
        else:              
            value = instruccion.interpretar(tree,table)
            if isinstance(value, Excepcion) :
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())