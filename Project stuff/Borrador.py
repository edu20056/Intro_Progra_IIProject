import pygame
from Editor import editor
#import time
#Listo

#____________________________________________Funciones de ventanas secundarias__________________________________________
def ventana_sec1():
    #Altura y ancho
    width, height = 600,600

    #Ventana secundaria
    ventana = pygame.display.set_mode((width,height))

    # Nombre ventana secundaria
    pygame.display.set_caption("Menú de aplicación")

    #Colores de objetos.
    ventana.fill((198,42,92))
    boton_color = (120,200,13)
    boton_color_encima = (75,109,29)
    texto_color = (255,255,255)
    color_negro = (0,0,0)

    # Colores matriz
    colors = {
        0: (255, 255, 255),  # Blanco
        1: (0, 0, 0),  # Negro
        2: (0, 255, 0)  # Verde
    }

    #Boton de pygame. Configura la fuente y el texto del botón
    boton = pygame.Rect(100,200, 400,100) #x , y , altura, ancho
    font = pygame.font.SysFont("Times New Roman", 30)
    button_text = font.render("Volver menú principal", True, texto_color)

    running = True
    while running:
        pygame.display.flip() #Actualizar pantalla

        pos_mouse = pygame.mouse.get_pos()
        if boton.collidepoint(pos_mouse):
            pygame.draw.rect(ventana, boton_color_encima, boton)
        else:
            pygame.draw.rect(ventana,boton_color, boton)

        # Dibuja el borde del botón
        pygame.draw.rect(ventana, color_negro, boton, 1)

        #Colocar texto
        texto_boton = button_text.get_rect(center = boton.center)
        ventana.blit(button_text, texto_boton)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton.collidepoint(pos_mouse):
                    running = False
                    ventana_principal()

#____________________________________________Ventana Principal__________________________________________________________
def ventana_principal():
    #Altura y ancho
    width, heigth = 800,800

    #Ventana
    ventana = pygame.display.set_mode((width,heigth))

    #Nombre ventana
    pygame.display.set_caption("Menú de aplicación")

    #Colores de objetos.
    ventana.fill((214, 88, 180)) #Color de ventana de fondo
    boton_color = (88,214,141)
    boton_color_encima = (20,106,56)
    texto_color = (255,255,255)
    color_negro = (0,0,0)

    #Colores matriz
    colors = {
        0: (255, 255, 255),  # Blanco
        1: (104,95,109), #Gris
        2: (0, 255, 0),  #Verde
        3: (248,12,12), #Rojo
        4: (237,248,12), #Amarillo
        5: (12,237,248), #Celeste
        6: (12,41,248), #Azul
        7: (151,9,242), #Morado
        8: (253, 19, 168),  #Rosado
        9: (0, 0, 0),  #Negro
    }

    #Boton de pygame. Configura la fuente y el texto del botón
    boton = pygame.Rect(200,650, 500,100) #x , y , altura, ancho
    font = pygame.font.SysFont("Times New Roman", 48)
    button_text = font.render("Abrir ventana secundaria", True, texto_color)

    def crear_botones_colores():
        botones = []
        x_start = 50  # Posición inicial x
        y = 70  # Posición fija y
        spacing = 70  # Espaciado entre botones

        for i in range(1,10):
            x = x_start + (i - 1) * spacing
            rec_base = pygame.Rect(x, y, 50, 50)
            pygame.draw.rect(ventana,colors[i], rec_base)
            pygame.draw.rect(ventana, color_negro, rec_base, 1)
            botones.append(rec_base)

        return botones
    crear_botones_colores()
    def dibujar_matriz(map):
        cell_size = 40  # Tamaño de cada celda
        offset_x = 50  # Offset en x para centrar la matriz
        offset_y = 150  # Offset en y para centrar la matriz
        for row in range(12):
            for col in range(12):
                color = colors[map[row][col]]
                pygame.draw.rect(ventana, color, pygame.Rect(col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size))
                pygame.draw.rect(ventana, color_negro, pygame.Rect(col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size), 1)

    mapa1 = editor("matriz_base.txt", "Eduardo", "en proceso")
    mapa_base = mapa1.matriz()
    mapa_base_trans = mapa1.transpuesta()
    dibujar_matriz(mapa_base)
    #dibujar_matriz(mapa_base_trans)

    running = True
    while running:
        pygame.display.flip() #Actualizar pantalla

        pos_mouse = pygame.mouse.get_pos()
        if boton.collidepoint(pos_mouse):
            pygame.draw.rect(ventana, boton_color_encima, boton)
        else:
            pygame.draw.rect(ventana,boton_color, boton)

        # Dibuja el borde del botón
        pygame.draw.rect(ventana, color_negro, boton, 1)

        #Colocar texto
        texto_boton = button_text.get_rect(center = boton.center)
        ventana.blit(button_text, texto_boton)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton.collidepoint(pos_mouse):
                    running = False
                    ventana_sec1()
#______________________________________________Inicio pygame____________________________________________________________
#Inicio pygame
pygame.init()

#Llamada ventana principal
ventana_principal()
