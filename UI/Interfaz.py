import re
import tkinter as tk
import webbrowser
from io import open
from tkinter import *
from tkinter import ttk, filedialog
import os

from Analizador.AnalizadorScript import AnalizadorLexico


class Interfaz:
    analizador = AnalizadorLexico()
    contenido = ""

    def cadenaError(self):
        cadena_temp = ""
        for error in self.analizador.listaErrores:
            cadena_temp += "<tr><td>"+str(error.descripcion)+"</td><td>"+str(error.linea)+"</td><td>"+str(error.columna)+"</td></tr>\n"
        return cadena_temp

    def cadenaTokens(self):
        cadena_temp = ""
        for token in self.analizador.listaTokens:
            cadena_temp += "<tr><td>"+str(token.lexema)+"</td><td>"+str(token.linea)+"</td><td>"+str(token.columna)+"</td></tr>\n"
        return cadena_temp

    def exportarReporteTokens(self):
        dir = os.getcwd()
        archivo = open(dir+"\\Modelos\\ModeloTokens.html", "r")
        modelo = archivo.read()
        archivo.close()
        pagina_resultado = open(dir+"\\Modelos\\tokens.html", "w+")
        indice = modelo.index("</table>")
        cadena = self.cadenaTokens()
        nuevo_contenido = ""
        nuevo_contenido += modelo[0:indice] + cadena[0] + modelo[indice:len(modelo)]
        indice2 = nuevo_contenido.rindex("</table>")
        nuevo_contenido = nuevo_contenido[:indice2] + cadena[1:] + nuevo_contenido[indice2:]
        pagina_resultado.write(nuevo_contenido)
        webbrowser.open_new_tab(dir+"\\Modelos\\tokens.html")

    def exportarReporteErrores(self):
        dir = os.getcwd()
        archivo = open(dir + "\\Modelos\\ModeloErrores.html", "r")
        modelo = archivo.read()
        archivo.close()
        pagina_resultado = open(dir + "\\Modelos\\errores.html", "w+")
        indice = modelo.index("</table>")
        cadena = self.cadenaError()
        nuevo_contenido = ""
        nuevo_contenido += modelo[0:indice] + cadena[0] + modelo[indice:len(modelo)]
        indice2 = nuevo_contenido.rindex("</table>")
        nuevo_contenido = nuevo_contenido[:indice2] + cadena[1:] + nuevo_contenido[indice2:]
        pagina_resultado.write(nuevo_contenido)
        webbrowser.open_new_tab(dir + "\\Modelos\\errores.html")

    def crearPagina(self):
        dir = os.getcwd()
        archivo = open(dir + "\\Modelos\\Principal.html", "r")
        modelo = archivo.read()
        archivo.close()
        pagina_resultado = open(dir + "\\Modelos\\index.html", "w+")
        indice = modelo.index("</iframe>")+10
        cadena = ""
        info = False
        if self.analizador.existeValor("entrada"):
            cadena += "\n<button onclick=\""+"entrada()"+"\">Click</button>\n"
        elif self.analizador.existeValor("info"):
            cadena += "\n<button onclick=\"" + "info()" + "\">Click</button>\n"
            info = True
        nuevo_contenido = ""
        nuevo_contenido += modelo[0:indice] + cadena[0] + modelo[indice:len(modelo)]
        indice2 = nuevo_contenido.rindex("</iframe>")+10
        nuevo_contenido = nuevo_contenido[:indice2] + cadena[1:] + nuevo_contenido[indice2:]
        pagina_resultado.write(nuevo_contenido)
        webbrowser.open_new_tab(dir + "\\Modelos\\index.html")
        if info is False:
            self.crearFormulario()
        else:
            self.crearInfo()

    def crearInfo(self):
        #     aqui creo el nuevo formulario
        dir = os.getcwd()
        archivo = open(dir + "\\Modelos\\Externa2.html", "r")
        modelo = archivo.read()
        archivo.close()
        pagina_resultado = open(dir + "\\Modelos\\iframe.html", "w+")
        indice = modelo.index("</p>") + 10
        cadena = "<p>"+self.texto_analizar.get('1.0', END)+"</p>"
        nuevo_contenido = ""
        nuevo_contenido += modelo[0:indice] + cadena[0] + modelo[indice:len(modelo)]
        indice2 = nuevo_contenido.rindex("</p>")
        nuevo_contenido = nuevo_contenido[:indice2] + cadena[1:] + nuevo_contenido[indice2:]
        pagina_resultado.write(nuevo_contenido)

    def crearFormulario(self):
        #  aqui creo el nuevo formulario
        dir = os.getcwd()
        archivo = open(dir + "\\Modelos\\Externa1.html", "r")
        modelo = archivo.read()
        archivo.close()
        pagina_resultado = open(dir + "\\Modelos\\iframe.html", "w+")
        indice = modelo.index("</form>")
        cadena = ""
        contador = 0
        for token in self.analizador.listaTokens:
            if token.lexema == "tipo" and "etiqueta" in self.analizador.listaTokens[contador+2].lexema:
                cadena += " <label>" + re.sub("\"", "", self.analizador.listaTokens[contador+6].lexema) + "</label><br>\n"
            elif token.lexema == "tipo" and "texto" in self.analizador.listaTokens[contador+2].lexema:
                cadena += "<input type=\"text\"  placeholder=\"" + re.sub("\"", "", self.analizador.listaTokens[contador+10].lexema) + "\"><br>\n"
            elif token.lexema == "tipo" and "grupo-option" in self.analizador.listaTokens[contador+2].lexema:
                cadena += "<select>\n"
                for token in self.analizador.listaTokens[contador+11:self.analizador.buscarCaracter("]", contador + 9):2]:
                    cadena += "<option >"+str(token.lexema)+"</option>+\n"
                cadena += "</select>"
            #     aqui mi codigo para grupo radio
            elif token.lexema == "tipo" and "grupo-radio" in self.analizador.listaTokens[contador + 2].lexema:
                id = 0
                for token in self.analizador.listaTokens[contador + 11:self.analizador.buscarCaracter("]", contador + 9):2]:
                    cadena += "<label> <input type=\"radio\">"+token.lexema+"<label>"
                    id += 1
            contador += 1
        nuevo_contenido = ""
        nuevo_contenido += modelo[0:indice] + cadena[0] + modelo[indice:len(modelo)]
        indice2 = nuevo_contenido.rindex("</form>")
        nuevo_contenido = nuevo_contenido[:indice2] + cadena[1:] + nuevo_contenido[indice2:]
        pagina_resultado.write(nuevo_contenido)

    def abrirArchivo(self, nombre):
        dir = os.getcwd()
        webbrowser.open_new_tab(dir + "\\Manuales\\"+nombre)

    def opElegida(self, event):
        if self.clicked.get() == "Reporte de tokens":
            self.exportarReporteTokens()
        elif self.clicked.get() == "Reporte de errores":
            self.exportarReporteErrores()
        elif self.clicked.get() == "Manual técnico":
            self.abrirArchivo("Manual técnico.pdf")
        elif self.clicked.get() == "Manual de usuario":
            self.abrirArchivo("Manual de usuario.pdf")

    def crearInterfaz(self):
        root = tk.Tk()
        root.geometry("1200x800")
        root.configure(background='#263D42')
        # creo el combo box del menu de reportes
        opciones = ["Reportes",
                    "Reporte de tokens",
                    "Reporte de errores",
                    "Manual de usuario",
                    "Manual técnico",
                    ]
        self.clicked = StringVar()
        self.clicked.set(opciones[0])
        self.combo = OptionMenu(root, self.clicked, *opciones, command=self.opElegida)
        self.combo.pack(pady=10)
        # creo el text area
        self.texto_analizar = Text(root, width=100, height=40)
        self.texto_analizar.pack(pady=40)

        # creo los botones
        boton_frame = Frame(root)
        boton_frame.pack()
        self.boton_analizar = Button(boton_frame, text="Analizar", command=self.analizarClick)
        self.boton_analizar.grid(row=0, column=0, padx=10)
        self.boton_cargar = Button(boton_frame, text="Cargar", command=self.cargarArchivo)
        self.boton_cargar.grid(row=0, column=1, padx=10)
        # boton guardar
        self.boton_guardar = Button(boton_frame, text="Guardar", command=self.guardarArchivo)
        self.boton_guardar.grid(row=0, column=2, padx=10)
        root.mainloop()

    def analizarClick(self):
        self.analizador.analizar(self.contenido)
        self.crearPagina()

    def guardarArchivo(self):
        ruta = tk.filedialog.asksaveasfilename()
        try:
            with open(ruta, 'w') as f:
                f.write(self.texto_analizar.get('1.0', END))
        except FileNotFoundError:
            print("No existe el directorio")

    def cargarArchivo(self):
        ruta = os.getcwd() + "\\Archivos Entrada"
        nombre_archivo = filedialog.askopenfilename(initialdir="ruta", title="Seleccionar un archivo",
                                                    filetypes=(("texto", "*.form"), ("todos", "*.*")))
        try:
            archivo = open(nombre_archivo, "r")
            self.contenido += archivo.read()
            self.texto_analizar.insert('1.0', self.contenido)
        except FileNotFoundError:
            print("archivo no encontrado")
