'''
TEC – Escuela de Ingeniería en Computadores
CE-1101 Introducción a la Programación. Grupo 01.
Proyecto II – Pixel Art Editor
Eduardo José Canessa Quesada & Luis Felipe Chaves Mena
'''

import pygame
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from screeninfo import get_monitors
import os
import copy

# < Configuración de la aplicación >
# __________________________________

# Ancho y alto de la app.
APPWIDTH = int(get_monitors()[0].width * 0.90)
APPHEIGHT = int(get_monitors()[0].height * 0.85)

# Definición de tasa de frecuancia de fotogramas.
FPS = 120

# Colores RGB asociados a números.
colors = {
    0: (255, 255, 255),  # Blanco
    1: (104, 95, 109),   # Gris
    2: (0, 255, 0),      # Verde
    3: (248, 12, 12),    # Rojo
    4: (237, 248, 12),   # Amarillo
    5: (12, 237, 248),   # Cian
    6: (12, 41, 248),    # Azul
    7: (151, 9, 242),    # Púrpura
    8: (253, 19, 168),   # Rosa
    9: (0, 0, 0),        # Negro
}

# Códigos ASCII.
codif = {
    0: " ",   # Espacio
    1: ".",   # Punto
    2: ":",   # Dos puntos
    3: "-",   # Guión
    4: "=",   # Igual
    5: "¡",   # Exclamación
    6: "&",   # Ampersand
    7: "$",   # Dólar
    8: "%",   # Porcentaje
    9: "@"    # Arroba
}

# Mapeo de teclas para el cambio de color. 
key_mapping = {
    pygame.K_0: 0,
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
    pygame.K_6: 6,
    pygame.K_7: 7,
    pygame.K_8: 8,
    pygame.K_9: 9
}

# < Definición de Clases >
# ________________________

class Canvas:

    """Clase Canvas
    
    < Atributos >
    
    // archivo : Ruta de acceso del archivo a cargar en el lienzo.
    // estado : Estado actual del lienzo ["En proceso", "Sin guardar"].
    // nombre : Nombre del archivo o "Nuevo Lienzo" si no hay archivo.
    // matrix : Matriz que representa el lienzo.

    < Métodos >

    ClockWise(matrix) : Rota la matriz en sentido horario.
    // input : matrix - Matriz a rotar.
    // output : Matriz rotada.
    // restric : (list of list of int)

    Anti_ClockWise(matrix) : Rota la matriz en sentido antihorario.
    // input : matrix - Matriz a rotar.
    // output : Matriz rotada.
    // restric : (list of list of int)

    Mirror_hrz(matrix) : Invierte la matriz horizontalmente.
    // input : matrix - Matriz a invertir.
    // output : Matriz invertida horizontalmente.
    // restric : (list of list of int)

    Mirror_vrt(matrix) : Invierte la matriz verticalmente.
    // input : matrix - Matriz a invertir.
    // output : Matriz invertida verticalmente.
    // restric : (list of list of int)

    Draw(matrix, color, coords) : Dibuja un punto en la matriz.
    // input : matrix - Matriz en la que se va a dibujar.
    //          color - Color del punto.
    //          coords - Coordenadas del punto.
    // output : Matriz con el punto dibujado.
    // restric : (list of list of int), (int color), (tuple coords)

    Negative(matrix) : Convierte la matriz a su negativo.
    // input : matrix - Matriz a convertir.
    // output : Matriz convertida.
    // restric : (list of list of int)

    HighCt(matrix) : Aplica alto contraste a la matriz.
    // input : matrix - Matriz a procesar.
    // output : Matriz con alto contraste.
    // restric : (list of list of int)

    Square(matrix, color) : Dibuja un cuadrado en la matriz.
    // input : matrix - Matriz en la que se va a dibujar.
    //          color - Color del cuadrado.
    // output : Matriz con el cuadrado dibujado.
    // restric : (list of list of int), (int color)

    Rhomb(matrix, color) : Dibuja un rombo en la matriz.
    // input : matrix - Matriz en la que se va a dibujar.
    //          color - Color del rombo.
    // output : Matriz con el rombo dibujado.
    // restric : (list of list of int), (int color)
    """

    def __init__(self, archivo):

        if archivo:
            self.archivo = archivo
            self.estado = "en proceso"
            self.nombre = os.path.basename(self.archivo) # Nombre del archivo, con base en su ruta.
        else:
            self.estado = "sin guardar"
            self.nombre = "Nuevo Lienzo" # Default nombre. 

        self.matrix = []
        with open(self.archivo, 'r') as file:
            txt_lines = file.readlines()
            for line in txt_lines:
                # Convierte cada línea en una lista de enteros.
                row = list(map(int, line.strip().split())) 
                if row:
                    # Agrega la fila a la matriz, siempre y cuando la lista no este vacía.
                    self.matrix.append(row)
        file.close()

    def ClockWise(self, matrix):

        res = []
        lista_aux = []

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):

                # Agregar elementos transpuestos a la lista auxiliar.
                lista_aux.append(matrix[j][i])

            # Agregar la lista auxiliar invertida a la lista de resultados.
            res.append(lista_aux[::-1])
            
            lista_aux = [] # Reiniciar la lista auxiliar para la siguiente fila.
        
        return res

    def Anti_ClockWise(self, result):

        res = []
        filas = len(result)
        columnas = len(result[0])

        for i in range(len(result)):
            # Lista para almacenar una nueva fila.
            nueva_fila = []
            for j in range(filas):

                 # Agregar el elemento correspondiente a la nueva fila en sentido antihorario.
                nueva_fila.append(result[j][columnas - 1 - i])
            
            # Agregar la nueva fila a la lista de resultados.
            res.append(nueva_fila)

        return res
    
    def Mirror_hrz(self, matrix):
    
        res = []
        
        for i in matrix:
            # Agregar la fila invertida a la lista de resultados.
            res.append(i[::-1])

        return res

    def Mirror_vrt(self, matrix):
    
        # Calcular la posición del último elemento de la matriz.
        pos = len(matrix) -1
        result = []
        
        while 0 <= pos:
            # Agregar la fila a la lista de resultados en orden inverso.
            result.append(matrix[pos])
            pos -= 1
        
        return result
    
    def Draw(self, matrix, color, coords) :

        # Obtener las coordenadas de la celda a colorear.
        row, col = coords
        matrix[row][col] = color # Cambiar el color de la celda en la matriz.
        
        return matrix 
    
    def Negative(self, matrix):

        res = []
        lista_aux = []

        for i in matrix:
            for j in i:

                # Calcular el negativo de cada elemento y agregarlo a la lista auxiliar.
                x = 9 - j
                lista_aux.append(x)

            res.append(lista_aux)
            lista_aux = []

        return res
    
    def HighCt(self, matrix):

        res = []
        lista_aux = []

        for i in matrix:
            for j in i:
                
                # Asignar 0 si el valor es menor que 5, de lo contrario, asignar 9.
                if j < 5:
                    x = 0
                else:
                    x = 9

                lista_aux.append(x)
            res.append(lista_aux)
            lista_aux = []
        
        return res

    def Square(self, matrix, color, full):
        
        # Calcular el tamaño del cuadrado -mitad del canvas-.
        square_size = len(matrix) // 2
        n = len(matrix)

        # Calcular los índices de inicio y fin para el cuadrado.
        start = (n - square_size) // 2
        end = start + square_size

        for i in range(start, end):
            for j in range(start, end):

                # Verificar si se desea dibujar un cuadrado completo o solo el borde.
                if full :
                    
                    if i <= start or i <= end - 1:
                        matrix[i][j] = color

                    elif j <= start or j <= end - 1:
                        matrix[i][j] = color
                else:

                    if i == start or i == end - 1:
                        matrix[i][j] = color

                    elif j == start or j == end - 1:
                        matrix[i][j] = color

        return matrix

    def Rhomb(self, matrix, color, full):
        
        # Calcular el centro de la matriz.
        center = len(matrix) // 2
        
        # Verificar si se desea dibujar un rombo completo o solo el borde.
        if full :
            for i in range(len(matrix)):
                for j in range(len(matrix)):

                    # Calcular la distancia manhattan desde el centro.
                    if abs(center - i) + abs(center - j) <= len(matrix) // 2 - 1 :
                        matrix[i][j] = color
        else:
            for i in range(len(matrix)):
                for j in range(len(matrix)):

                    # Calcular la distancia manhattan desde el centro.
                    if abs(center - i) + abs(center - j) == len(matrix) // 2 - 1 :
                        matrix[i][j] = color

        return matrix

class Button:

    """Clase Button
        
    < Atributos >

    // coords : Coordenadas del centro del botón.
    // size : Tamaño del botón -cuadrado-.
    // color_off : Color del botón cuando está inactivo.
    // color_on : Color del botón cuando se activa.
    // command : Función a ejecutar cuando se presiona el botón.
    // surface : Superficie del botón -pygame Surface-.
    // rect : Rectángulo que delimita el botón -pygame Rect-.
    // photo : Ruta de la imagen para mostrar en el botón.
    // font : Fuente del texto del botón -pygame Font-.
    // text : Texto del botón.
    // font_color : Color del texto del botón.
    // text_surface : Superficie del texto del botón -pygame Surface-.
    // text_rect : Rectángulo que delimita el texto del botón -pygame Rect-.

    < Métodos >

    Over() : Con base en la posición del mouse, se determina el estado del botón activado/desactivado.
    A su vez también cambia el color del objeto. 

    Display(screen) : Muestra el botón en la pantalla.
    // input : screen - Superficie de la pantalla -pygame Surface-.

    // IMPORTANTE : Resulta más sencillo colocar el objeto en la pantalla general que ajustar los valores de coordenadas a una Superficie específica.

    Exe(*args) : Ejecuta la función asignada al botón cuando se presiona.
    // input : *args - Argumentos para la función asignada al botón.
    // output : Resultado de la función asignada al botón (depende de la función).
    """

    def __init__(self, coords, size, up=[100, 100, 100], down= None, command= None, text= " ", font= "Times New Roman", f_size= 16, f_color= [0, 0, 0], photo= None):

        self.coords = coords
        self.color_off = up
        self.size = size
        self.command = command
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(center=self.coords)
        self.photo = photo

        if down:
            self.color_on = down
        else:
            self.color_on = up

        self.font = pygame.font.SysFont(font, f_size)
        self.text = text
        self.font_color = f_color
        self.text_surface = self.font.render(self.text, 1, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=[i // 2 for i in self.size])

    def Over(self):
        
        # Cambiar el color actual al color apagado.
        self.color = self.color_off

        pos = pygame.mouse.get_pos() # Obtener la posición del mouse.
        
        if self.rect.collidepoint(pos):
            # Si hay colisión, cambiar el color actual al color encendido.
            self.color = self.color_on

    def Display(self, screen):
        
        # Verificar si el mouse está sobre el objeto y actualizar su color.
        self.Over()

         # Llenar la superficie del objeto con su color actual.
        self.surface.fill(self.color)

        # Este objeto da prioridad a las imagenes, por lo que no se desplegará ningún texto si existe una imagen. 
        if self.photo:

            screen.blit(self.surface, self.rect)

            # Cargar la imagen y ajustar su tamaño.
            image = pygame.image.load(self.photo)
            scaled_image = pygame.transform.scale(image, self.size)

            # Obtener el rectángulo de la imagen y centrarlo en el rectángulo del objeto.
            image_rect = scaled_image.get_rect(center=self.rect.center)
            screen.blit(scaled_image, image_rect.topleft)
        
        else:

            # Dibujar el texto en su superficie.
            self.surface.blit(self.text_surface, self.text_rect)
            screen.blit(self.surface, self.rect)
    
    def Exe(self, *args):

        # Verificar si hay un comando asignado al objeto.
        if self.command:

             # Ejecutar el comando con los argumentos proporcionados y devolver el resultado.
            return self.command(*args)

class Editor:

    """Clase Editor
        
    < Atributos >

    // width : Ancho de la ventana del editor.
    // height : Alto de la ventana del editor.
    // path : Ruta del archivo cargado en el editor.
    // status : Estado del archivo cargado en el editor ["In progress", "Not saved"].
    // name : Nombre del archivo cargado en el editor.
    // Canvas : Objeto Canvas que representa el lienzo del editor.
    // matrix : Matriz producto del Objeto Canvas.
    // save : Copia de seguridad de la matriz original del lienzo.
    // zoom_index : Índice de zoom actual del lienzo.
    // brush : Color de pincel actual.
    // edge : Booleano que indica si se muestran los bordes del lienzo.
    // font : Fuente de texto utilizada en el editor -pygame Font-.
    // clock : Reloj de pygame para controlar la velocidad de actualización.
    // screen : Superficie de la pantalla del editor -pygame Surface-.
    // canvas_surface : Superficie del lienzo del editor -pygame Surface-.
    // colorMenu_surface : Superficie del menú de colores del editor -pygame Surface-.
    // optsMenu_surface : Superficie del menú de opciones del editor -pygame Surface-.

    < Métodos >

    Grid(grid) : Crea y muestra la cuadrícula del lienzo en la superficie del lienzo.
    // input : grid - Matriz que representa el lienzo.
    // output : Lista de rectángulos que representan cada celda de la cuadrícula -list of pygame Rect-, 
    //          Coordenadas de cada celda de la cuadrícula -list of list of int-.
    // restric : (list of list of int).

    Zoom(surface, zoom_factor) : Aplica un factor de zoom a una superficie.
    // input : surface - Superficie a la que aplicar el zoom.
    //          zoom_factor - Factor de zoom.
    // output : Superficie con el zoom aplicado -pygame Surface-.
    // restric : El zoom es condicionado en Exe().

    ColorMenu(surface) : Crea y muestra el menú de colores en la superficie de menú de colores.
    // input : surface - Superficie del menú de colores.
    // output : Lista de rectángulos que representan los botones de colores list of -pygame Rect-.
    // restric : (pygame Surface).

    Paint(plane, canvas, canvas_rect) : Aplica el color de pincel en la posición del cursor en la matriz del lienzo.
    // input : plane - Matriz que representa el lienzo.
    //          canvas - Objeto Canvas que representa el lienzo.
    //          canvas_rect - Rectángulo del lienzo en la pantalla.
    // output : Matriz actualizada con el color de pincel aplicado.
    // restric : (list of list of int), (obj Canvas), (pygame Rect).

    PrintCore(core, encode) : Muestra la matriz del lienzo en una ventana emergente, además codifica para ASCII de ser necesario.
    // input : core - Matriz que representa el lienzo.
    //          encode - Booleano que indica si se codifican los valores de la matriz a ASCII. 
    // output : Ventana emergente con la matriz. 
    // restric : (list of list of int), (bool).

    OpenFile() : Abre un archivo de texto y carga su contenido en el editor.

    SaveFile() : Guarda el contenido actual del lienzo en un archivo de texto.

    Exe() : Ejecuta el bucle principal del editor.
    Se definen botones, eventos, etc. 

    """

    def __init__(self, path= None, font= ("Times New Roman", 14), edge= True):
    
        # Definir el ancho y alto de la ventana. 
        self.width = APPWIDTH
        self.height = APPHEIGHT

        # Configuración del proyecto. 
        if path:
            # Si se proporciona una ruta, establecer el estado del proyecto como "En progreso" y obtener el nombre del archivo.
            self.path = path
            self.status = "In progress"
            self.name = os.path.basename(self.path)
        else:
            # Si no se proporciona una ruta, establecer la ruta predeterminada, el estado como "No guardado" y el nombre como "Nuevo Proyecto".
            self.path = "Draft.txt"
            self.status = "Not saved"
            self.name = "New Proyect"

        # Inicialización del lienzo y la matriz del proyecto.
        self.Canvas = Canvas(self.path)
        self.matrix = self.Canvas.matrix
        self.save = copy.deepcopy(self.Canvas.matrix)

        # Inicialización de variables para el zoom, el pincel y los bordes.
        self.zoom_index = 1.0
        self.brush = 0
        self.edge = edge

        # Inicialización de pygame y configuración de la ventana. 
        pygame.init()
        pygame.display.set_icon(pygame.image.load("Images/logo.png"))
        self.font = pygame.font.SysFont(font[0], font[1])
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"{self.name} [{len(self.matrix)}x{len(self.matrix)}] - ({self.status})")

        # Creación de las superficies.

        # Lienzo.
        self.canvas_surface = pygame.Surface((int(self.width * 0.90), self.height))
        self.canvas_surface.fill((30, 30, 30))

        # Menú de Colores. 
        self.colorMenu_surface = pygame.Surface((int(self.width * 0.05), int(self.height * 0.75)))
        self.colorMenu_surface.fill((48, 48, 48))

        # Menú de Opciones. 
        self.optsMenu_surface = pygame.Surface((int(self.width * 0.15), self.height))
        self.optsMenu_surface.fill((48, 48, 48))

    def Grid(self, grid):

        list_matrix = []
        coords_matrix = []

        # Tamaño de celda basado en la altura del lienzo y el tamaño de la matriz.
        cell_size = self.canvas_surface.get_height() // len(self.matrix)
        
        for row in range(len(grid)):
            for col in range(len(grid[0])):

                # Obtener el color de la celda. 
                color = colors[grid[row][col]]

                # Calcular la posición izquierda y superior de la celda en el lienzo.
                left = (col * cell_size) + (self.canvas_surface.get_width() - len(self.matrix[0]) * cell_size) // 2
                top = (row * cell_size) + (self.canvas_surface.get_height() - len(self.matrix) * cell_size) // 2

                # Dibujar un rectángulo en el lienzo con el color correspondiente
                rec = pygame.draw.rect(self.canvas_surface, color, pygame.Rect(left, top, cell_size, cell_size))
                
                # Dibujar los bordes si está habilitado. 
                if self.edge:
                    pygame.draw.rect(self.canvas_surface, (150, 150, 150), pygame.Rect(left, top, cell_size, cell_size), 1)
                
                # Almacenar las coordenadas y el objeto rectángulo en las listas. 
                coords_matrix.append([row, col])
                list_matrix.append(rec)

        return list_matrix, coords_matrix

    def Zoom(self, surface, zoom_factor):

        # Calcular el nuevo ancho y alto de la superficie escalada. 
        width = int(surface.get_width() * zoom_factor)
        height = int(surface.get_height() * zoom_factor)

        # Escalar la superficie utilizando la función transform.scale de pygame. 
        return pygame.transform.scale(surface, (width, height))
    
    def ColorMenu(self, surface):

        # Lista para almacenar los botones circulares. 
        button_list = []

        # Calcular el radio del botón basado en el ancho de la superficie.
        radius = int(surface.get_width() * 0.20)
        # Definir la posición inicial en el eje Y y el espaciado entre los botones.
        y_start = int(surface.get_height() * 0.065)
        spacing = int(surface.get_height() * 0.10)
        # Calcular la posición X central.
        x = int(surface.get_width() // 2)

        for j in range(len(colors)):

            # Posición Y del botón actual.
            y = y_start + j * spacing
            # Calcular el centro del botón. 
            center = (x, y)
            # Crear un rectángulo base para el botón
            rec_base = pygame.Rect(0, j * surface.get_height() // 10 + surface.get_height() * 0.195, surface.get_width(), surface.get_height() // 10) 
            # Dibujar un círculo en la superficie con el color correspondiente
            pygame.draw.circle(surface, colors[j], center, radius)

            button_list.append(rec_base)

        return button_list

    def Paint(self, plane, canvas, canvas_rect):

        pos_mouse = pygame.mouse.get_pos()
        # Ajustar la posición del ratón a la escala actual del lienzo.
        pos_mouse_adj = ((pos_mouse[0] - canvas_rect.left) / self.zoom_index, (pos_mouse[1] - canvas_rect.top) / self.zoom_index)
        
        # Obtener la matriz de celdas y las coordenadas de la cuadrícula. 
        matrix, coords = self.Grid(plane) 

        for rec in matrix:
            # Verificar si el mouse colisiona con el rectángulo actual. 
            if rec.collidepoint(pos_mouse_adj):

                # Obtener el índice del rectángulo en la matriz. 
                i = matrix.index(rec)

                # Dibujar en el lienzo la celda con el pincel seleccionado en las coordenadas correspondientes. 
                plane = canvas.Draw(plane, self.brush, coords[i])

                return plane
        return plane

    def PrintCore(self, core, encode):

         # Crear y configura una ventana de la biblioteca Tkinter.
        display = tk.Tk()
        display.title(f"{self.name} [{len(self.matrix)}x{len(self.matrix)}] - Core ")
        display.iconbitmap("Images/icon.ico")
        display.config(background= "white")

        # Crear un lienzo dentro de la ventana. 
        canvas = tk.Canvas(display, background= "white")
        canvas.pack(side="left", fill="both", expand=True)

        # Crear una barra de desplazamiento vertical para el Canvas. 
        y_scrollbar = tk.Scrollbar(display, orient="vertical", command=canvas.yview)
        # Vincular el evento de configuración del Canvas para actualizar la región de desplazamiento.
        y_scrollbar.pack(side="right", fill="y")

         # Configurar el lienzo para que use la barra de desplazamiento vertical.
        canvas.configure(yscrollcommand=y_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Crear un Frame dentro del Canvas. 
        frame = tk.Frame(canvas, background= "white")
        canvas.create_window((display.winfo_width() // 2, display.winfo_height() // 2), window=frame, anchor="center")

        for i, row in enumerate(core):
            for j, val in enumerate(row):
                cell_font = ("Times New Roman", 16, "bold")

                # Codificar o convertir el valor en cadena según el parámetro de codificación. 
                if encode:
                    element = codif[val]
                else:
                    element = str(val)

                # Crear una etiqueta de Tkinter para representar cada celda. 
                cell = tk.Label(frame, text= element, font=cell_font, borderwidth= 0, relief= "solid", width= 1, height= 1, fg= "black", background= "white")
                cell.grid(row= i, column= j, padx= 5, pady= 5)

        display.mainloop()
    
    def OpenFile(self): 

        # Abrir un cuadro de diálogo para seleccionar un archivo de texto. 
        file_path = askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

         # Verificar si se seleccionó un archivo. 
        if file_path:

            # Iniciar un nuevo editor con el archivo seleccionado y ejecutarlo. 
            pygame.quit()
            Editor(path= file_path).Exe()

    def SaveFile(self):

        # Abrir un cuadro de diálogo para guardar un archivo, con extensión .txt por defecto. 
        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        # Verificar si se seleccionó un destino de archivo. 
        if file_path:

            # Abrir el archivo en modo de escritura. 
            with open(file_path, 'w') as file:

                # Convertir la matriz a líneas de texto y escribir en el archivo. 
                lines = [" ".join(map(str, row)) for i, row in enumerate(self.matrix)]
                content = "\n".join(lines)
                file.write(content)

            # Actualizar la información de la ruta y el estado del archivo guardado.
            self.path = file_path
            self.status = "In progress"
            self.name = os.path.basename(self.path)
            # Actualizar el título de la ventana de Pygame con el nombre del archivo y su tamaño.
            pygame.display.set_caption(f"{self.name} [{len(self.matrix)}x{len(self.matrix)}] - ({self.status})")
                
            # Cerrar el archivo después de escribir.
            file.close()

    def Exe(self):
        
        # Calcula las coordenadas centrales del lienzo. 
        canvas_x = self.canvas_surface.get_width() // 2
        canvas_y = self.canvas_surface.get_height() // 2

        # Calcula el tamaño de los botones en función del ancho de la superficie de opciones. 
        button_size = int(self.optsMenu_surface.get_width() * 0.15)
        
        # Crea instancias de botones con diferentes configuraciones. 
        highContrs = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.925, APPHEIGHT * 0.25), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/highContrast.png")
        negative = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.75, APPHEIGHT * 0.25), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/negative.png")
        
        edge_b = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.585), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/edge.png")
        see_matrix = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.635), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/display.png")
        see_ascii = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.685), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/display.png")

        shape_squrd = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.60, APPHEIGHT * 0.80), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/square.png")
        shape_diam = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.80), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/rombo.png")
        full_squrd = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.80, APPHEIGHT * 0.80), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/full_square.png")
        full_diam = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.20, APPHEIGHT * 0.80), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/full_rombo.png")

        turnRight = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.20, APPHEIGHT * 0.90), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/right.png")
        turnLeft = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.80, APPHEIGHT * 0.90), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/left.png")
        mirrorVert = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.60, APPHEIGHT * 0.90), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/mirrorV.png")
        mirrorHorz = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.90), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/mirrorH.png")

        return_b = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.125, APPHEIGHT * 0.25), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/return.png")

        # Lista de todos los botones creados. 
        button_list = [turnRight, turnLeft, mirrorVert, mirrorHorz, highContrs, negative, edge_b, full_squrd, shape_squrd, shape_diam, full_diam, see_matrix, see_ascii, return_b]

        running = True
        while running:

            # Limpia la pantalla. 
            self.screen.fill((30, 30, 30))

            # Dibuja la cuadrícula en la pantalla.
            self.Grid(self.matrix)

            # Escala el lienzo y lo coloca en la pantalla. 
            scaled_canvas = self.Zoom(self.canvas_surface, self.zoom_index)
            canvas_rect = scaled_canvas.get_rect(center=(canvas_x, canvas_y))
            self.screen.blit(scaled_canvas, canvas_rect)

            # Muestra & lista del menú de colores.
            clrs = self.ColorMenu(self.colorMenu_surface)
            self.screen.blit(self.colorMenu_surface, (0, int(self.height * 0.25) // 2))

            # Muestra un cuadro de muestra del color seleccionado. 
            sample = pygame.Rect(0, int(self.optsMenu_surface.get_height() * 0.075), self.optsMenu_surface.get_width(), int(self.optsMenu_surface.get_height() * 0.15) )    
            pygame.draw.rect(self.optsMenu_surface, colors[self.brush], sample)
            self.screen.blit(self.optsMenu_surface, (int(self.width * 0.85), 0))

            # Titulo : Color RGB. 
            color_title = self.font.render(f"{colors[self.brush]}", True, (255, 255, 255))
            color_title_rect = color_title.get_rect(topright=(self.screen.get_width() - 5, APPHEIGHT * 0.035))
            self.screen.blit(color_title, color_title_rect)

            # Titulo : Bordes. 
            edge_title = self.font.render("EDGES", True, (255, 255, 255))
            edge_title_rect = edge_title.get_rect(topleft=(APPWIDTH * 0.875, APPHEIGHT * 0.575))
            self.screen.blit(edge_title, edge_title_rect)

            # Titulo : Nomral Matrix Display. 
            normal_title = self.font.render("NOR.M.D.", True, (255, 255, 255))
            normal_title_rect = normal_title.get_rect(topleft=(APPWIDTH * 0.875, APPHEIGHT * 0.625))
            self.screen.blit(normal_title, normal_title_rect)

            # Titulo : ASCII Matrix Display. 
            ascii_title = self.font.render("A.S.C.I.I.", True, (255, 255, 255))
            ascii_title_rect = ascii_title.get_rect(topleft=(APPWIDTH * 0.875, APPHEIGHT * 0.675))
            self.screen.blit(ascii_title, ascii_title_rect)

            # Titulo : Figuras. 
            shapes_title = self.font.render("SHAPES", True, (255, 255, 255))
            shapes_title_rect = shapes_title.get_rect(topleft=(APPWIDTH * 0.875, APPHEIGHT * 0.745))
            self.screen.blit(shapes_title, shapes_title_rect)

            # Muestra los botones en la pantalla. 
            for b in button_list:
                b.Display(self.screen)


            # Controla la apariencia del pincel según la posición del mouse.
            pos_mouse = pygame.mouse.get_pos()
            if self.colorMenu_surface.get_width() < pygame.mouse.get_pos()[0] < int(APPWIDTH * 0.80):
                pygame.mouse.set_visible(False)
                brush_size = self.canvas_surface.get_height() // (2 * len(self.matrix)) * self.zoom_index
                pygame.draw.circle(self.screen, colors[self.brush], pos_mouse, brush_size, 3)
            else:
                pygame.mouse.set_visible(True)

            # Control de Eventos. 
            for event in pygame.event.get():

                # Exit App. 
                if event.type == pygame.QUIT:
                    running = False

                # Eventos asociados a teclas presionadas. 
                elif event.type == pygame.KEYDOWN:
                    
                    # Exit App. 
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    # Manejo de movimiento del lienzo con las teclas de flecha.
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if canvas_x > 0:
                            canvas_x -= 50
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if canvas_x < self.canvas_surface.get_width():
                            canvas_x += 50
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        if canvas_y > 0:
                            canvas_y -= 50
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if canvas_y < self.canvas_surface.get_height():
                            canvas_y += 50

                    # Cambio del color en uso según las teclas definidas en key_mapping. 
                    if event.key in key_mapping:
                        current_value = key_mapping[event.key]
                        self.brush = current_value

                    # Manejo de comandos con CTRL. 
                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        
                        # Zoom In : CTRL++, CTRL+=.
                        if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                            if self.zoom_index < 1.6:
                                self.zoom_index += 0.1
                        
                        # Zoom Out: CTRL+-.
                        elif event.key == pygame.K_MINUS:
                            if self.zoom_index > 0.4:
                                self.zoom_index -= 0.1
                        
                        # Go back : CTRL+Z.
                        elif event.key == pygame.K_z:
                            self.matrix = copy.deepcopy(self.save)
                        # Save Proyect : CTRL+S.
                        elif event.key == pygame.K_s:
                            self.SaveFile()
                        # Open Proyect : CTRL+O.
                        elif event.key == pygame.K_o:
                            self.OpenFile()
                        # Cover all Canvas : CTRL+SPACE.
                        elif event.key == pygame.K_SPACE:
                            self.matrix = [[self.brush for _ in row] for row in self.matrix]

                # Manejo de eventos con mouse.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Click Izquierdo. 

                        # Seleccionar color del menú de colores. 
                        for color, button in enumerate(clrs):
                            if button.collidepoint(pos_mouse):
                                self.brush = color  

                        # Controlar acciones según el botón presionado. 
                        for b in button_list:
                            if b.rect.collidepoint(pos_mouse):
                                if b == turnRight:
                                    self.matrix = self.Canvas.ClockWise(self.matrix)
                                elif b == turnLeft:
                                    self.matrix = self.Canvas.Anti_ClockWise(self.matrix)
                                elif b == mirrorVert:
                                    self.matrix = self.Canvas.Mirror_vrt(self.matrix)
                                elif b == mirrorHorz:
                                    self.matrix = self.Canvas.Mirror_hrz(self.matrix)
                                elif b == highContrs:
                                    self.save = copy.deepcopy(self.matrix)
                                    self.matrix = self.Canvas.HighCt(self.matrix)
                                elif b == negative:
                                    self.save = copy.deepcopy(self.matrix)
                                    self.matrix = self.Canvas.Negative(self.matrix)
                                elif b == shape_squrd:
                                    self.matrix = self.Canvas.Square(self.matrix, self.brush, False)
                                elif b == shape_diam:
                                    self.matrix = self.Canvas.Rhomb(self.matrix, self.brush, False)
                                elif b == full_squrd:
                                    self.matrix = self.Canvas.Square(self.matrix, self.brush, True)
                                elif b == full_diam:
                                    self.matrix = self.Canvas.Rhomb(self.matrix, self.brush, True)
                                elif b == see_matrix:
                                    self.PrintCore(self.matrix, False)
                                elif b == see_ascii:
                                    self.PrintCore(self.matrix, True)
                                elif b == edge_b:
                                    self.edge = not self.edge
                                elif b == return_b:
                                    self.matrix = copy.deepcopy(self.save)
                    
                    if event.button == 3: # Click Derecho. 
                        # Restablecer el color a blanco. 
                        self.brush = 0

                    # Control del zoom con la rueda del mouse. 
                    if event.button == 4: # In. 
                        if self.zoom_index < 1.6: # Restricciones del Zoom. 
                            self.zoom_index += 0.1
                    
                    elif event.button == 5: # Out. 
                        if self.zoom_index > 0.4: # Restricciones del Zoom. 
                            self.zoom_index -= 0.1

            # Pintar en el lienzo si se mantiene presionado el botón izquierdo del mouse. 
            if pygame.mouse.get_pressed()[0]:
                self.matrix = self.Paint(self.matrix, self.Canvas, canvas_rect)

            # Actualizar la pantalla, de acuerdo con FPS.         
            pygame.display.update()
            self.clock.tick(FPS)    

        # Salir del bucle principal al cerrar la ventana. 
        pygame.quit()

# Run. 
if __name__ == '__main__':
    Editor().Exe()