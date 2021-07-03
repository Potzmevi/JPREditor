from Instrucciones.Continue import Continue
from Abstract.Instruccion import Instruccion
from Instrucciones.Break import Break
from TS.Excepcion         import Excepcion
from TS.Tipo              import TIPO
from TS.TablaSimbolos     import TablaSimbolos
from Abstract.NodoAST import NodoAST

class Case(Instruccion):
    def __init__(self, expresion, instrucciones, fila, columna):
        self.expresion         = expresion
        self.instrucciones     = instrucciones
        self.fila              = fila
        self.columna           = columna


        

    def interpretar(self, tree, table):

        nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
        for instruccion in self.instrucciones:
            nuevaTabla.setEntorno("Switch-Case")
            result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL CASE
            if isinstance(result, Excepcion):
                tree.getExcepciones().append(result)
                tree.updateConsola(result.toString())
            if isinstance(result, Break): return True
            if isinstance(result, Continue): return True



    def getNodo(self):
        nodo = NodoAST("Case")
        instrucciones = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo 
