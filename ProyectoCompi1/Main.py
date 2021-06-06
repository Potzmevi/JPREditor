from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import ttk

# Variables globales
# Path del archivo en memoria
archivo = ""   
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
# Nuevo archivo
def nuevo():   
    global archivo
    editor.delete(1.0, END)
    archivo = ""
# Abrir archivo
def abrir():       
    global archivo
    archivo = filedialog.askopenfilename(title = "Abrir Archivo", initialdir = "C:/",filetypes=[("jpr files", ".jpr")])
    entrada = open(archivo)
    content = entrada.read()
    editor.delete(1.0, END)
    editor.insert(INSERT, content)
    entrada.close()
    lineas()
# Guardar archivo
def guardarArchivo():  
    global archivo
    if archivo == "":
        guardarComo()
    else:
        guardarc = open(archivo, "w")
        guardarc.write(editor.get(1.0, END))
        guardarc.close()
# Guardar archivo como
def guardarComo():      
    global archivo
    guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "C:/",filetypes=[("jpr files", ".jpr")],defaultextension='.jpr')
    
    fguardar = open(guardar, "w+")
    fguardar.write(editor.get(1.0, END))
    fguardar.close()
    archivo = guardar
    

# Declaracion del tk
raiz = Tk()

# Frame principal
frame = Frame(raiz, bg="gray12")
frame.grid(sticky='news')
# Canvas
canvas = Canvas(frame, bg="gray12")
canvas.grid(row=0, column=1)
# Frame del canvas
ventana = Frame(canvas, bg="gray12")
canvas.create_window((0, 0), window=ventana, anchor="nw")
canvas.configure(width=1150, height=700)

# Componentes
# Label de fila y columna
lbPosicion= Label(ventana, text="Fila: 0, Columna: 0",width=76)
lbPosicion.grid(column=0, row=3,sticky="nw",padx=25,pady=50)
# Label de resultado
lbResultado= Label(ventana, text="Resultado del interprete",width=71)
lbResultado.grid(column=1, row=3,sticky="nw",padx=0,pady=50)
# ScrolledText del editor
editor = scrolledtext.ScrolledText(ventana, undo=True, width=60, height=15,background='grey35',foreground='white')
editor.grid(column=0, row=3, pady=75, padx=60)
# ScrolledText de la consola
console = scrolledtext.ScrolledText(ventana, undo=True, width=60, height=15,background='black',foreground='SpringGreen2')
console.grid(column=1, row=3, pady=75, padx=0,sticky="w")
# Canvas de fila del editor
lines = Canvas(ventana, width=30, height=240, background='gray60')
lines.grid(column=0, row=3,padx=25,sticky="w")
# Boton de analizar
photo = PhotoImage(file = "Resources\compilarIcono.png")
boton1= Button(ventana,text="Analizar",width=100,height=50,image = photo,background='grey12')
boton1.grid(row=0,column=1,sticky="e")
# Menu bar
menu = Menu(ventana)
# Archivo
new_item = Menu(menu,tearoff=0)
new_item.add_command(label='Nuevo',command=nuevo)
new_item.add_command(label='Abrir',command=abrir)
new_item.add_command(label='Guardar',command=guardarArchivo)
new_item.add_command(label='Guardar como',command=guardarComo)
menu.add_cascade(label='Archivo', menu=new_item)
# Analizar
new_item = Menu(menu,tearoff=0)
new_item.add_command(label='Analizar')
menu.add_cascade(label='Analizar', menu=new_item)
# Reportes
new_item = Menu(menu,tearoff=0)
new_item.add_command(label='Simbolos')
new_item.add_command(label='Errores')
menu.add_cascade(label='Reportes', menu=new_item)
raiz.config(menu=menu)

#Titulo
Label(ventana,text="JPR Editor",font="Helvetica 15",foreground='DodgerBlue2',background='gray12').grid(row=0,column=0,sticky="e")
#Label Tabla de Simbolos
Label(ventana,text="Tabla de Simbolos",font="Helvetica 15",foreground='green2',background='gray12').grid(row=4,column=0)
#Label Tabla de Errores
Label(ventana,text="Tabla de Errores",font="Helvetica 15",foreground='red2',background='gray12').grid(row=4,column=1)

#Tabla De Simbolos
tv=ttk.Treeview(ventana,height=7)
tv['columns']=('#', 'Identificador', 'Tipo', 'Dimension', 'Valor', 'Ambito', 'Referencias')
tv.column('#0', width=0, stretch=NO)
tv.column('#', anchor=CENTER, width=10)
tv.column('Identificador', anchor=CENTER, width=100)
tv.column('Tipo', anchor=CENTER, width=100)
tv.column('Dimension', anchor=CENTER, width=80)
tv.column('Valor', anchor=CENTER, width=80)
tv.column('Ambito', anchor=CENTER, width=80)
tv.column('Referencias', anchor=CENTER, width=85)
tv.heading('#0', text='', anchor=CENTER)
tv.heading('#', text='#', anchor=CENTER)
tv.heading('Identificador', text='Identificador', anchor=CENTER)
tv.heading('Tipo', text='Tipo', anchor=CENTER)
tv.heading('Dimension', text='Dimension', anchor=CENTER)
tv.heading('Valor', text='Valor', anchor=CENTER)
tv.heading('Ambito', text='Ambito', anchor=CENTER)
tv.heading('Referencias', text='Referencias', anchor=CENTER)
tv.insert(parent='', index=0, iid=0, text='', values=('1','Vineet','Alpha'))
tv.insert(parent='', index=1, iid=1, text='', values=('2','Anil','Bravo'))
tv.insert(parent='', index=2, iid=2, text='', values=('3','Vinod','Charlie'))
tv.insert(parent='', index=3, iid=3, text='', values=('4','Vimal','Delta'))
tv.insert(parent='', index=4, iid=4, text='', values=('5','Manjeet','Echo'))
tv.grid(column=0, row=5,padx=25,pady=15,sticky="w")

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
tv1.insert(parent='', index=0, iid=0, text='', values=('1','Vineet','Alpha'))
tv1.insert(parent='', index=1, iid=1, text='', values=('2','Anil','Bravo'))
tv1.insert(parent='', index=2, iid=2, text='', values=('3','Vinod','Charlie'))
tv1.insert(parent='', index=3, iid=3, text='', values=('4','Vimal','Delta'))
tv1.insert(parent='', index=4, iid=4, text='', values=('5','Manjeet','Echo'))
tv1.grid(row=5,column=1,pady=15)

#Estilo tabla
style=ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background="grey35",
    foreground='white',
    fieldbackground="grey35")

style.map('Treeview',background=[('selected','DodgerBlue2')])


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

# Main loop
raiz.mainloop()
