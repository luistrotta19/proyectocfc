from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import re

########################## Desarrollo Interfaz Gráfica  ############################################
root = Tk()
root.title("Curvas de Tracción")
root.geometry("770x450")


id = StringVar()
velocidad = StringVar()
fuerza = StringVar()
resistencia = StringVar()
fuerzag = StringVar()

# ###########################    Conectar con Base de Datos ##########################################
def conexionBBDD():
    miConexion = sqlite3.connect("curvas.db")
    miCursor = miConexion.cursor()

    try:
        miCursor.execute(
            "CREATE TABLE tablafv(id INTEGER PRIMARY KEY, velocidad, fuerza, resistencia,fuerzag)"
        )
        messagebox.showinfo("CONEXION", "Base de Datos Creada Exitosamente")
    except:
        messagebox.showinfo("CONEXION", "Conexión exitosa con la base de datos")


def salir_aplicacion():
    valor = messagebox.askquestion("Salir", "¿Esta seguro que desea salir?")
    if valor == "yes":
        root.destroy()


def limpiarCampos():
    id.set("")
    velocidad.set("")
    fuerza.set("")
    resistencia.set("")
    fuerzag.set("")


def mensaje():
    acerca = """
    Aplicación CURVAS
    Version 1.0
    Tecnología Python Tkinter
    Autores: Luis Trotta, Jeronimo Espora.
    
     Funciones:
    Menú inicio: 
    Crear/Conectar base de datos: crea la base de de datos para trabajar la primera vez, conecta las subsiguientes veces.
    Salir: cierra el programa.

    Botones:
    Limpiar: Limpia los campos de registros.
    Calcular: "FUNCIóN EN DESARROLLO" (esta función permitirá calcular la diferencia entre los valores de la fuerza y la resistencia)
    Crear: Crea el registro con los valores de campos asignados en la base de datos. (los valores del registro fuerza solo se cargan efectivamente si son valores numéricos de hasta 3 dígitos)
    Modificar: Después de seleccionar un registro con doble click, se editan los valores en los campos y con el botón modificar se guardan los nuevos valores.
    Eliminar registro: Después de seleccionar un registro con doble click, elimina permanentemente el registro de la base de datos.
    Mostrar lista: Muestra los valores de los registros almacenados en la base de datos en la tabla. 
    """
    messagebox.showinfo(title="INFORMACIÖN", message=acerca)


########################################   Métodos     CRUD      #################################################################


def crear():

    cadena = velocidad.get()
    patron = "^[0-9]{1,3}$"
    print(velocidad.get())

    if re.match(patron, cadena):

        lab6 = Label(root, text="Valor en rango          ")
        lab6.place(x=230, y=10)
        miConexion = sqlite3.connect("curvas.db")
        miCursor = miConexion.cursor()

        try:

            datos = (velocidad.get(), fuerza.get(), resistencia.get(), fuerzag.get())
            print(fuerzag.get())
            fuerza_g = fuerza.get()
            print(fuerza_g)
            miCursor.execute("INSERT INTO tablafv VALUES(NULL,?,?,?,?)", (datos))
            miConexion.commit()

        except:
            messagebox.showwarning(
                "ADVERTENCIA",
                "Ocurrió un error al crear el registro, verifique conexión con BBDD",
            )
        pass
    else:
        lab7 = Label(root, text="Valor fuera de Rango")
        lab7.place(x=230, y=10)

    limpiarCampos()
    mostrar()


def calcular():
    miConexion = sqlite3.connect("curvas.db")
    miCursor = miConexion.cursor()
    valor = miCursor.execute("SELECT* FROM tablafv;")
    # valor=len(miCursor.fetchall())
    print(type(valor))

    for row in valor:
        print(row)

        calc_val = str(int(row[2]) - int(row[3]))
        print(calc_val)
        sql = (
            "UPDATE tablafv SET velocidad="
            + str(row[1])
            + ", fuerza="
            + str(row[2])
            + ", resistencia="
            + str(row[3])
            + ", fuerzag="
            + str(int(row[2]) - int(row[3]))
            + " WHERE  id="
            + str(row[0])
        )

        # datos = (row[0],row[1], row[2], row[3], row[4])
        # print (row[0],row[1], fuerzag)
        # sql= "UPDATE tablafv SET velocidad=?, fuerza=?, resistencia=? , fuerzag=?, id=row[0] "
        miCursor.execute(sql)

    miConexion.commit()


def mostrar():
    miConexion = sqlite3.connect("curvas.db")
    miCursor = miConexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        miCursor.execute("SELECT* FROM tablafv")
        for row in miCursor:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
    except:
        pass


####################################   Tabla   #######################################################

tree = ttk.Treeview(height=8, columns=("#0", "#1", "#2", "#3", "#4"))
tree.place(x=0, y=175)
tree.column("#0", width=50, anchor="center")
tree.column("#1", anchor="center")
tree.column("#2", anchor="center")
tree.column("#3", anchor="center")
tree.column("#4", width=100, anchor="center")

tree.heading("#0", text="ID", anchor=CENTER)
tree.heading("#1", text="Velocidad")  # , anchor=CENTER)
tree.heading("#2", text="Fuerza en Llanta", anchor=CENTER)
tree.heading("#3", text="Resistencia", anchor=CENTER)
tree.heading("#4", text="Fuerza Gancho", anchor=CENTER)


def seleccionarUsandoClick(event):
    item = tree.identify("item", event.x, event.y)
    id.set(tree.item(item, "text"))
    velocidad.set(tree.item(item, "values")[0])
    fuerza.set(tree.item(item, "values")[1])
    resistencia.set(tree.item(item, "values")[2])
    fuerzag.set(tree.item(item, "values")[3])


tree.bind("<Double-1>", seleccionarUsandoClick)


def actualizar():
    miConexion = sqlite3.connect("curvas.db")
    miCursor = miConexion.cursor()
    try:

        datos = (velocidad.get(), fuerza.get(), resistencia.get(), fuerzag.get())
        miCursor.execute(
            "UPDATE tablafv SET velocidad=?, fuerza=?, resistencia=?, fuerzag=? WHERE ID="
            + id.get(),
            (datos),
        )
        """
        for row in valor:
            cal_val= int(row[2]) - int(row[3])
            print (cal_val)
            miCursor.execute(
            "UPDATE tablafv SET velocidad=row[1], fuerza=row[2], resistencia=row[3], fuerzag=calc_val WHERE ID="
            )
        """
        miConexion.commit()
    except:
        messagebox.showwarning(
            "ADVERTENCIA", "Ocurrió un error al actualizar el registro"
        )
        pass
    limpiarCampos()
    mostrar()


def borrar():
    miConexion = sqlite3.connect("curvas.db")
    miCursor = miConexion.cursor()
    try:
        if messagebox.askyesno(
            message="¿ Realmente desea eliminar el registros?", title="ADVERTENCIA"
        ):
            miCursor.execute("DELETE FROM tablafv WHERE ID=" + id.get())
            miConexion.commit()
    except:
        messagebox.showwarning(
            "ADVERTENCIA", "Ocurrió un error al tratar de eliminar el registro"
        )
        pass
    limpiarCampos()
    mostrar()


################################### Crear Widgets en la VISTA ########################################

####################### Creando Menú ###################
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar base de datos", command=conexionBBDD)
# menubasedat.add_command(label= "Eliminar  base de datos", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salir_aplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)


ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Acerca de ", command=mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

root.config(menu=menubar)

##############################  Creando Etiquetas y Cajas de Texto #######################
e1 = Entry(root, textvariable=id)

lab2 = Label(root, text="Velocidad")  # , justify=CENTER)
lab2.place(x=20, y=10)
e2 = Entry(root, textvariable=velocidad, width=12)  # , justify=CENTER)
e2.place(x=140, y=10)


lab3 = Label(root, text="Fuerza en la Llanta")
lab3.place(x=20, y=40)
e3 = Entry(root, textvariable=fuerza, width=12)
e3.place(x=140, y=40)

lab4 = Label(root, text="Resistencia Loc.")
lab4.place(x=20, y=70)
e4 = Entry(root, textvariable=resistencia, width=12)
e4.place(x=140, y=70)

lab5 = Label(root, text="Fuerza en el Gancho")
lab5.place(x=20, y=100)
e5 = Entry(root, textvariable=fuerzag, width=12)
e5.place(x=140, y=100)

############################## Creando Botones ####################################
b1 = Button(root, text="Crear Registro", command=crear)
b1.place(x=250, y=130)

b2 = Button(root, text="Modificar Registro", command=actualizar)
b2.place(x=400, y=130)

b3 = Button(root, text="Mostrar Lista", command=mostrar)
b3.place(x=90, y=415)

b4 = Button(root, text="Eliminar Registro", bg="red", command=borrar)
b4.place(x=575, y=130)

b5 = Button(root, text="Limpiar", bg="yellow", command=limpiarCampos)
b5.place(x=250, y=50)

b6 = Button(root, text="Calcular", bg="yellow", command=calcular)
b6.place(x=350, y=50)

root.config(menu=menubar)
root.mainloop()
