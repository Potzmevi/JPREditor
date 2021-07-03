import os
import re
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog as FileDialog
from tkinter import messagebox
from tkinter import ttk
from TS.TablaSimbolos import TablaSimbolos
from gramatica import analizarTexto as compilar
from gramatica import getErrores as errores
from PIL import Image
from gramatica import getSimbolos as simbolos
from gramatica import getFunciones as funciones


# Recorrer el texto para separar palabras por colores
def recorrerInput(i):  
    lista = []
    val = ''
    counter = 0
    while counter < len(i):
            if re.search(r"[a-z|0-9|.|A-Z]", i[counter]):
                val += i[counter]
            elif i[counter] == "\"":
                if len(val) != 0:
                    l = []
                    l.append("cadena")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = i[counter]
                counter += 1
                
                while counter < len(i):
                    if i[counter] == "\"":
                        val += i[counter]
                        l = []
                        l.append("cadena")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += i[counter]
                    counter += 1
            elif i[counter] == "#":
                if len(val) != 0:
                    l = []
                    l.append("comentario")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = i[counter]
                counter += 1
                if i[counter] == "*":
                   while counter < len(i):
                        if i[counter] == "#":
                            val += i[counter]
                            l = []
                            l.append("comentario")
                            l.append(val)
                            lista.append(l)
                            val = ''
                            break
                        val += i[counter]
                        counter += 1 
                else:    
                    while counter < len(i):
                        if i[counter] == "\n":
                            val += i[counter]
                            l = []
                            l.append("comentario")
                            l.append(val)
                            lista.append(l)
                            val = ''
                            break
                        val += i[counter]
                        counter += 1
            elif i[counter] == "\'":
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = i[counter]
                counter += 1
                while counter < len(i):
                    if i[counter] == "\'":
                        val += i[counter]
                        l = []
                        l.append("cadena")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += i[counter]
                    counter += 1
            else:
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                l = []
                l.append("otro")
                l.append(i[counter])
                lista.append(l)
            counter +=1
    for s in lista:
        if s[1] == 'var' or s[1] == 'func' or s[1] == 'read' or s[1] == 'tolower' or s[1] == 'toupper' or s[1] == 'lenght' or s[1] == 'truncate' or s[1] == 'round' or s[1] == 'typeof' or s[1] == 'return' or s[1] == 'break' or s[1] == 'switch' or s[1] == 'case' or s[1] == 'default' or s[1] == 'false' or s[1] == 'true' or s[1] == 'while' or s[1] == 'for' or s[1] == 'continue' or  s[1] == 'else' or s[1] == 'if' or s[1] == 'null' or s[1] == 'boolean' or s[1] == 'string' or s[1] == 'int' or s[1] == 'double' or s[1] == 'char' or s[1] == 'print' or s[1] == 'main':
            s[0] = 'reservada'
        elif re.search(r'\d+',s[1]) or re.search(r'\d+\.\d+',s[1]):
            if re.search(r'\".*?\"',s[1]):
                s[0] = 'cadena'
            elif re.search(r'\#\*(.|\n)*?\*\#|\#.*\n',s[1]):
                s[0] = 'comentario'
            elif re.search(r'[a-z|A-Z]',s[1]):
                s[0]= "otro"
            else:
                s[0] = 'numero'
        elif re.search(r'\".*?\"',s[1]):
            s[0] = 'cadena'
        elif re.search(r'\#\*(.|\n)*?\*\#|\#.*\n',s[1]):
            s[0] = 'comentario'
    return lista

# Metodos
# Actualizar lineas
def lineas(*args):
    lines.delete("all")

    cont = editor.index("@1,0")
    while True:
        dline = editor.dlineinfo(cont)
        if dline is None:
            break
        y = dline[1]
        strline = str(cont).split(".")[0]
        lines.create_text(2, y, anchor="nw", text=strline,
                          font=("Consolas", 10))
        cont = editor.index("%s+1line" % cont)

# Actualizar posicion
def posicion(event=None):
    lbPosicion.config(
        text="Linea: " + str(editor.index(INSERT)).replace(".", ", Columna: "))


# Llamar metodos
def llamarMetodos(event):
    posicion()
    lineas()
    
# Exportar errores
def exportar_errores():
    archivo = "tablaErrores.dot"
    salida = "digraph errores {\n"
    salida += "tbl [\n shape = plaintext, color=cornflowerblue,fillcolor=beige, style=filled,fontname = \"helvetica\"\n"
    salida += "label=<\n"
    salida += "<table  >\n"
    salida += "<tr> <td colspan='5'>Reporte de Errores</td> </tr> \n"
    salida += "<tr> <td> </td> <td>Tipo</td> <td>Descripcion</td> <td>Linea</td> <td>Columna</td> </tr> \n"
    excepciones = errores()
    cont = 1
    for excepcion in excepciones:
        salida += "<tr> <td>"+str(cont)+"</td> <td>"+excepcion.getTipo()+"</td> <td>"+excepcion.getDescripcion()+"</td> <td>"+str(excepcion.getFila())+"</td> <td>"+str(excepcion.getColumna())+"</td> </tr> \n"
        cont += 1
    salida += "</table>\n"
    salida += ">];\n"
    salida += "}"
    
    with open(archivo,'w') as f:
        f.write(salida) 
    
    os.system('dot -Tpng '+archivo+' -o imagen.png')
    os.startfile("imagen.png")
    
# Exportar Simbolos
def exportar_simbolos():
    archivo = "tablaSimbolos.dot"
    salida = "digraph simbolos {\n"
    salida += "tbl [\n shape = plaintext, color=cornflowerblue,fillcolor=beige, style=filled,fontname = \"helvetica\"\n"
    salida += "label=<\n"
    salida += "<table  >\n"
    salida += "<tr> <td colspan='10'>Tabla de simbolos</td> </tr> \n"
    salida += "<tr> <td> </td> <td>Nombre</td> <td>Tipo</td> <td>Tipo2</td> <td>Ambito</td> <td>Valor</td> <td>Linea</td> <td>Columna</td> </tr> \n"
    listasimbolos = simbolos()
    listafunciones = funciones()
    cont = 1
    for simbolo in listasimbolos:
        salida += "<tr> <td>"+str(cont)+"</td> <td>"+simbolo.getID()+"</td> <td>"+"Variable"+"</td> <td>"+str(simbolo.getTipo())+"</td> <td>"+str(simbolo.getEntorno())+"</td> <td>"+str(simbolo.getValor())+"</td> <td>"+str(simbolo.getFila())+"</td> <td>"+str(simbolo.getColumna())+"</td></tr> \n"
        cont += 1
    salida += "</table>\n"
    salida += ">];\n"
    salida += "}"
    
    with open(archivo,'w') as f:
        f.write(salida) 
    
    os.system('dot -Tpng '+archivo+' -o simbolos.png')
    os.startfile("simbolos.png")

# Declaracion del tk
raiz = Tk()
raiz.title("JPR Editor")
# Frame principal
frame = Frame(raiz, bg="gray60")
frame.grid(sticky='news')
# Canvas`
canvas = Canvas(frame, bg="gray60")
canvas.grid(row=0, column=1)
# Frame del canvas
ventana = Frame(canvas, bg="gray60")
canvas.create_window((0, 0), window=ventana, anchor="nw")
canvas.configure(width=1300, height=650)

# Componentes
# Label de fila y columna
lbPosicion= Label(ventana, text="Fila: 0, Columna: 0",width=90)
lbPosicion.grid(column=0, row=3,sticky="nw",padx=25,pady=25)
# ScrolledText del editor
editor = scrolledtext.ScrolledText(ventana, undo=True, width=65, height=15)
editor.grid(column=0, row=3, pady=50, padx=40,sticky="e")
# ScrolledText de la consola
console = scrolledtext.ScrolledText(ventana, undo=True, width=60, height=15,background='black',foreground='SpringGreen2')
console.grid(column=1, row=3, pady=50, padx=0)
# Canvas de fila del editor
lines = Canvas(ventana, width=30, height=240, background='gray60')
lines.grid(column=0, row=3,padx=25,sticky="w")


#Titulo
Label(ventana,text="JPR Editor",background='SpringGreen4',font="Helvetica 15").grid(row=0,column=0,sticky="e")
#Label Tabla de Simbolos
Label(ventana,text="Tabla de Simbolos",background='SpringGreen4',font="Helvetica 15").grid(row=4,column=0)
#Label Tabla de Errores
Label(ventana,text="Tabla de Errores",background='SpringGreen4',font="Helvetica 15").grid(row=4,column=1)
#Label Contador de compilacion
Label(ventana,text="0",font="Helvetica 15",background='gray60').grid(row=2,column=1)

#Tabla De Simbolos
tv=ttk.Treeview(ventana,height=7)
tv['columns']=('#', 'Identificador', 'Tipo', 'Tipo2', 'Entorno', 'Valor', 'Linea','Columna')
tv.column('#0', width=0, stretch=NO)
tv.column('#', anchor=CENTER, width=10)
tv.column('Identificador', anchor=CENTER, width=80)
tv.column('Tipo', anchor=CENTER, width=80)
tv.column('Tipo2', anchor=CENTER, width=80)
tv.column('Entorno', anchor=CENTER, width=80)
tv.column('Valor', anchor=CENTER, width=80)
tv.column('Linea', anchor=CENTER, width=120)
tv.column('Columna', anchor=CENTER, width=120)
tv.heading('#0', text='', anchor=CENTER)
tv.heading('#', text='#', anchor=CENTER)
tv.heading('Identificador', text='Identificador', anchor=CENTER)
tv.heading('Tipo', text='Tipo', anchor=CENTER)
tv.heading('Tipo2', text='Tipo2', anchor=CENTER)
tv.heading('Entorno', text='Entorno', anchor=CENTER)
tv.heading('Valor', text='Valor', anchor=CENTER)
tv.heading('Linea', text='Linea', anchor=CENTER)
tv.heading('Columna', text='Columna', anchor=CENTER)
tv.grid(column=0, row=5,padx=25,sticky="w")

#Tabla Reporte de errores
tv1=ttk.Treeview(ventana,height=7)
tv1['columns']=('#', 'Tipo', 'Descripcion', 'Linea', 'Columna')
tv1.column('#0', width=0, stretch=NO)
tv1.column('#', anchor=CENTER, width=10)
tv1.column('Tipo', anchor=CENTER, width=100)
tv1.column('Descripcion', anchor=CENTER, width=250)
tv1.column('Linea', anchor=CENTER, width=70)
tv1.column('Columna', anchor=CENTER, width=70)
tv1.heading('#0', text='', anchor=CENTER)
tv1.heading('#', text='#', anchor=CENTER)
tv1.heading('Tipo', text='Tipo', anchor=CENTER)
tv1.heading('Descripcion', text='Descripcion', anchor=CENTER)
tv1.heading('Linea', text='Linea', anchor=CENTER)
tv1.heading('Columna', text='Columna', anchor=CENTER)
tv1.grid(row=5,column=1)

def analizar():
    texto=compilar(editor.get(1.0,END))
    console.delete(1.0, "end")
    console.insert(INSERT,texto)
    listaerrores=errores()
    listasimbolos=simbolos()
    listafunciones=funciones()
    contador=1
    contador2=1
    tv1.delete(*tv1.get_children())
    for error in listaerrores:
        tv1.insert(parent='', index=contador, iid=contador, text='', values=(contador,error.getTipo(),error.getDescripcion(),error.getFila(),error.getColumna()))
        contador+=1
    tv.delete(*tv.get_children())
    for simbolo in listasimbolos:
        tv.insert(parent='', index=contador2, iid=contador2, text='', values=(contador2,simbolo.getID(),"Variable",simbolo.getTipo(),simbolo.getEntorno(),simbolo.getValor(),simbolo.getFila(),simbolo.getColumna()))
        contador2+=1
    for simbolo in listafunciones:
         if simbolo.getNombre()=="round" or simbolo.getNombre()=="toupper" or simbolo.getNombre()=="tolower" or simbolo.getNombre()=="length" or simbolo.getNombre()=="truncate" or simbolo.getNombre()=="typeof":
            continue
         else:
            tv.insert(parent='', index=contador2, iid=contador2, text='', values=(contador2,simbolo.getNombre(),"Funcion",simbolo.getTipo(),"Global","-",simbolo.getFila(),simbolo.getColumna()))
            contador2+=1
    contenidocolor= editor.get(1.0, END)
    editor.delete(1.0, "end")
    for s in recorrerInput(contenidocolor):
        editor.insert(INSERT, s[1], s[0])
    
    
    

#BOTON COMPILAR
boton1= Button(ventana,text="Compilar",width=25,command=analizar)
boton1.grid(row=3,column=1,sticky="n")

# Acciones del teclado
editor.bind('<Return>', llamarMetodos)
editor.bind('<BackSpace>', llamarMetodos)
editor.bind('<<Change>>', llamarMetodos)
editor.bind('<Configure>', llamarMetodos)
editor.bind('<Motion>', llamarMetodos)
editor.bind('<KeyPress>', posicion)
editor.bind('<Button>', posicion)
editor.bind('<Key>', llamarMetodos)
editor.bind('<Enter>', llamarMetodos)

#Estilo tabla
style=ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    fieldbackground="#D3D3D3")

style.map('Treeview',background=[('selected','SpringGreen4')])


#Definimos la variable ruta
ruta=""
#Nuevo Archivo
def nuevo():
    global ruta
    ruta = ""
    editor.delete(1.0, "end")
    raiz.title("JPR Editor")
    
def abrirast():
    os.startfile("ast.pdf")
    
#Abrir Archivo
def abrir():
    global ruta
    ruta = FileDialog.askopenfilename(
        initialdir='.', 
        filetypes=(("Ficheros de texto", "*.jpr"),),
        title="Abrir un fichero de texto")

    if ruta != "":
        fichero = open(ruta, 'r')
        contenido = fichero.read()
        editor.delete(1.0,'end')
        for s in recorrerInput(contenido):
            editor.insert(INSERT, s[1], s[0])
        fichero.close()
        raiz.title(ruta + " - JPR Editor")

#GUARDAR
def guardar():
    if ruta != "":
        contenido = editor.get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        messagebox.showinfo(message="Archivo guardado",title="Mensaje")
        contenidocolor= editor.get(1.0, END)
        editor.delete(1.0, "end")
        for s in recorrerInput(contenidocolor):
            editor.insert(INSERT, s[1], s[0])
    else:
        guardar_como()

#GUARDAR COMO
def guardar_como():
    global ruta
    fichero = FileDialog.asksaveasfile(title="Guardar fichero", 
        mode="w", defaultextension=".jpr")
    if fichero is not None:
        ruta = fichero.name
        contenido = editor.get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        messagebox.showinfo(message="Fichero guardado correctamente",title="Mensaje")
        contenidocolor= editor.get(1.0, END)
        editor.delete(1.0, "end")
        for s in recorrerInput(contenidocolor):
            editor.insert(INSERT, s[1], s[0])
    else:
        messagebox.showinfo(message="Guardado cancelado",title="Mensaje")
        ruta = ""


# Menu bar
menu = Menu(ventana)
new_item = Menu(menu,tearoff=0)
new_item.add_command(label='Nuevo', command=nuevo)
new_item.add_command(label='Abrir',command=abrir)
new_item.add_command(label='Guardar',command=guardar)
new_item.add_command(label='Guardar Como', command=guardar_como)
menu.add_cascade(label='Archivo', menu=new_item)
new_item2 = Menu(menu,tearoff=0)
new_item2.add_command(label='Errores', command=exportar_errores)
new_item2.add_command(label='Ast', command=abrirast)
new_item2.add_command(label='Tabla simbolos', command=exportar_simbolos)
menu.add_cascade(label='Reportes', menu=new_item2)
raiz.config(menu=menu)



# Tags para pintar el textos
editor.tag_config('reservada', foreground='RoyalBlue1')
editor.tag_config('cadena', foreground='orange2')
editor.tag_config('numero', foreground='purple1')
editor.tag_config('comentario', foreground='gray')
editor.tag_config('otro', foreground='black')


# Main loop
raiz.mainloop()