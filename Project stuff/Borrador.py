import pygame
from Editor import editor

#____________________________________________Variables globales_________________________________________________________
global n
n = 0

#____________________________________________Menú de juego______________________________________________________________
def ventana_menu():
        #Altura y ancho
    width, height = 600,600

    #Ventana secundaria
    ventana = pygame.display.set_mode((width,height))
    ventana.fill((0,0,255))

    # Nombre ventana secundaria
    pygame.display.set_caption("Menú de aplicación")

    #Colores
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

    def botones_menu():
        bot = []
        x = 120
        y_in = 10
        for i in range(3):
            y = y_in + i * 200
            rec = pygame.Rect(x , y, 350,150 )
            pygame.draw.rect(ventana,colors[7], rec)
            pygame.draw.rect(ventana, colors[9], rec, 1)

            bot.append(rec)
        return bot
    botones = botones_menu()
    running = True
    while running:
        lista_textos = ["Nuevo dibujo", "Cargar dibujo", "Salir de aplicacion"]
        font = pygame.font.SysFont("Times New Roman", 48)
        pos_mouse = pygame.mouse.get_pos()
        for boton in botones:
            if boton.collidepoint(pos_mouse):
                pygame.draw.rect(ventana, colors[4], boton)
            else:
                pygame.draw.rect(ventana,colors[7], boton)
                
        for i in range(3): #Escribir los textos 
            bot_tex = font.render(lista_textos[i], True, colors[9])
            texto_boton = bot_tex.get_rect(center = botones[i].center)
            ventana.blit(bot_tex, texto_boton)


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, boton in enumerate(botones):
                    if boton.collidepoint(pos_mouse):
                        if i == 0:
                            direccion = "Project stuff/matriz_base.txt"
                            nuevo_dibujo(direccion) # type: ignore #Abrir pantalla de dibujo con matriz limpia (matriz_base)
                            running = False
                        elif i == 1:
                            cargar() #Abrir ventana donde se podrá escribir un texto que indique la posicion de la matriz que se desee cargar.
                            running = False
                        else:
                            running = False

        pygame.display.flip()

#____________________________________________Funcion Escribir Matriz en txt______________________________________________
def escribir_matriz_en_txt(matriz, nombre_archivo):
    ruta = r'C:\Users\ejcan\Documents\GitHub\Intro_Progra_IIProject\Project stuff\\' + nombre_archivo
    with open(ruta, 'w') as archivo:
        for fila in matriz:
            linea = ', '.join(map(str, fila))
            linea_formateada = f'[{linea}]'
            archivo.write(linea_formateada + '\n')

#____________________________________________Ventana Cargar juego_______________________________________________________
def cargar():
    width, height = 600, 400

    ventana = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Escribir nombre y dibujo por cargar')
    font = pygame.font.SysFont("Times New Roman", 32)
    
    # Colores
    colors = {
        0: (255, 255, 255),  # Blanco
        1: (104, 95, 109),   # Gris
        2: (0, 255, 0),      # Verde
        3: (248, 12, 12),    # Rojo
        4: (237, 248, 12),   # Amarillo
        5: (12, 237, 248),   # Celeste
        6: (12, 41, 248),    # Azul
        7: (151, 9, 242),    # Morado
        8: (253, 19, 168),   # Rosado
        9: (0, 0, 0),        # Negro
    }
    text_box_nom = pygame.Rect(100, 100, 400, 50)
    activo_nom = False
    text_box_dir = pygame.Rect(100, 300, 400, 50)
    activo_dir = False
    text_dir = ''
    text_nom = ''
    
    running = True
    while running:
        lista_textos =["Coloque aquí el nuevo nombre para el dibujo.","Coloque la dirección de dibujo."]
        x = 250
        y_in = 20
        for i in range(1):
            y = y_in + i* 200
            rec = pygame.Rect(x, y, 100,100)
            button_text = font.render(lista_textos[i], True, colors[9])
            texto_boton = button_text.get_rect(center = rec.center)
        for i in range(1,2):
            y = y_in + i* 200
            rec = pygame.Rect(x, y, 100,100)
            button_text2 = font.render(lista_textos[i], True, colors[9])
            texto_boton1 = button_text2.get_rect(center = rec.center)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si el usuario hace clic en la caja de entrada
                if text_box_nom.collidepoint(event.pos):
                    activo_nom = True
                    activo_dir = False
                elif text_box_dir.collidepoint(event.pos):
                    activo_dir = True
                    activo_nom = False
                else:
                    activo_dir = False
                    activo_nom = False
            color_nom = colors[5] if activo_nom else colors[0]
            color_dir = colors[3] if activo_dir else colors[7]
            if event.type == pygame.KEYDOWN:

                if activo_nom:
                    if event.key == pygame.K_BACKSPACE:
                        text_nom = text_nom[:-1]
                    else:
                        text_nom += event.unicode

                elif activo_dir:
                    if event.key == pygame.K_BACKSPACE:
                        text_dir = text_dir[:-1]
                    else:
                        text_dir += event.unicode
                elif event.key == pygame.K_RETURN:
                    base_path = r"C:\Users\ejcan\Documents\GitHub\Intro_Progra_IIProject\Project stuff\\"
                    direccion = base_path + text_dir + ".txt"
                    print(direccion)
                    ventana_principal(direccion,text_nom)
                    running = False

        # Rellenar la ventana
        ventana.fill((18, 253, 189))
        
        ventana.blit(button_text, texto_boton)
        ventana.blit(button_text2, texto_boton1)
        # Dibujar la caja de texto
        pygame.draw.rect(ventana, color_nom, text_box_nom, 2)
        pygame.draw.rect(ventana, color_dir, text_box_dir, 2)
        
        # Renderizar el texto
        txt_surface = font.render(text_nom, True, colors[9])
        ventana.blit(txt_surface, (text_box_nom.x + 5, text_box_nom.y + 5))

        # Renderizar el texto
        txt_surface = font.render(text_dir, True, colors[9])
        ventana.blit(txt_surface, (text_box_dir.x + 5, text_box_dir.y + 5))
        
        pygame.display.flip()

#____________________________________________Ventana Nuevo Juego________________________________________________________
def nuevo_dibujo(direccion):
    width, height = 600, 400

    ventana = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Escribir nombre')
    font = pygame.font.SysFont("Times New Roman", 32)
    
    # Colores
    colors = {
        0: (255, 255, 255),  # Blanco
        1: (104, 95, 109),   # Gris
        2: (0, 255, 0),      # Verde
        3: (248, 12, 12),    # Rojo
        4: (237, 248, 12),   # Amarillo
        5: (12, 237, 248),   # Celeste
        6: (12, 41, 248),    # Azul
        7: (151, 9, 242),    # Morado
        8: (253, 19, 168),   # Rosado
        9: (0, 0, 0),        # Negro
    }

    text_box = pygame.Rect(100, 100, 400, 50)
    active = False
    color = colors[0]
    text = ''

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si el usuario hace clic en la caja de entrada
                if text_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = colors[5] if active else colors[0]
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        # Guardar el texto en una variable
                        texto_ingresado = text
                        running = False  # Salir del bucle después de presionar Enter
                        ventana_principal(direccion, texto_ingresado)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Rellenar la ventana
        ventana.fill((128, 53, 89))
        
        # Dibujar la caja de texto
        pygame.draw.rect(ventana, color, text_box, 2)
        
        # Renderizar el texto
        txt_surface = font.render(text, True, colors[9])
        ventana.blit(txt_surface, (text_box.x + 5, text_box.y + 5))
        
        pygame.display.flip()

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
    button_text = font.render("Salir", True, texto_color)

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
                    #ventana_principal()

#____________________________________________Ventana Principal__________________________________________________________
def ventana_principal(direccion, nombre): 
    #Altura y ancho
    width, heigth = 1200,800

    #Ventana
    ventana = pygame.display.set_mode((width,heigth))

    #Nombre ventana
    pygame.display.set_caption("Dibujo")

    #Colores de objetos.
    ventana.fill((214, 88, 180)) #Color de ventana de fondo
    boton_color = (88,214,141)
    boton_color_encima = (20,106,56)
    texto_color = (0,0,0)
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
    # Lista de botones asociados a las imágenes

    #Font texto
    font = pygame.font.SysFont("Times New Roman", 20)

    #Boton para salir y guardar.
    boton_fin = pygame.Rect(910,650, 250,70) #x , y , altura, ancho
    button_text = font.render("Guardar y volver al menú", True, texto_color)
    
    #Boton para mostrar la matriz numérica actual.
    boton_ver_matriz = pygame.Rect(50, 650, 200, 70 )

    #Boton para esconder la matriz numérica actual.
    boton_hide_matriz = pygame.Rect(260, 650, 200, 70 )

    #Boton girar izquierda
    boton_izq = pygame.Rect(540, 150, 100,75)

    #Boton girar derecha
    boton_der = pygame.Rect(540, 250, 100, 75)

    #Boton girar horizontal
    boton_hor = pygame.Rect(540, 350, 100, 75)

    #Boton girar vertical
    boton_vert = pygame.Rect(540,450, 100, 75)

    #Boton negativo de dibujo.
    boton_neg = pygame.Rect(540, 550, 100, 75)
    neg_text = font.render("Negativo", True, texto_color)

    #Boton zoom in
    boton_zoomin = pygame.Rect(660, 150, 100 , 75)

    #Boton zoom out
    boton_zoomout = pygame.Rect(660, 250, 100, 75)

    #Boton ASCI ver
    boton_ascii_ver = pygame.Rect(660, 350, 100 ,75)
    
    #Boton ASCI ver
    boton_ascii_hide = pygame.Rect(660, 450, 100 ,80)

    #Boton cuadrado
    boton_cuadr = pygame.Rect(470,650, 150,70) 

    #Boton rombo
    boton_romb = pygame.Rect(630,650, 150,70)

    #Boton alto contraste
    boton_contr = pygame.Rect(785, 650, 120, 70)
    contraste_text = font.render("Alto contraste", True, texto_color)

    #Boton cerrar imagen.
    boton_cerrar = pygame.Rect(660, 550, 100 ,75)

    #Lista de botones de dibujo
    lista_botones = [boton_fin, boton_ver_matriz, boton_hide_matriz, boton_der,boton_izq,boton_vert, boton_hor, boton_neg, boton_romb, boton_cuadr, boton_cerrar, boton_zoomin, boton_zoomout, boton_ascii_hide, boton_ascii_ver, boton_contr]

    #Listas de botones alineados horizontalmente y verticalmente. Se necesita para la colocacion iterativa de imagenes
    lista_botones_con_imagenes = [ boton_izq, boton_der, boton_hor, boton_vert, boton_ver_matriz, boton_hide_matriz, boton_cuadr, boton_romb, boton_cerrar, boton_zoomin ,boton_zoomout, boton_ascii_hide, boton_ascii_ver]

    #Lista de botones asociados al texto.
    botones_y_textos = [(boton_fin, button_text),(boton_neg, neg_text), (boton_contr, contraste_text)]
    
    imagenes = [
        #Listos
            #Verticales
        pygame.image.load("Project stuff/Imagenes/izquierda.png"),
        pygame.image.load("Project stuff/Imagenes/derecga.png"),
        pygame.image.load("Project stuff/Imagenes/flecha_hor.png"),
        pygame.image.load("Project stuff/Imagenes/flecha_vert.png"),
            #Horizontales
        pygame.image.load("Project stuff/Imagenes/ver_num.png"),
        pygame.image.load("Project stuff/Imagenes/quitar_num.png"),
        pygame.image.load("Project stuff/Imagenes/cuadrado.png"),
        pygame.image.load("Project stuff/Imagenes/rombo.png"),
        pygame.image.load("Project stuff/Imagenes/borrador.png"),

        #Faltan
        pygame.image.load("Project stuff/Imagenes/lupa_mas.png"),
        pygame.image.load("Project stuff/Imagenes/lupa_menos.png"),  
        pygame.image.load("Project stuff/Imagenes/ASCII.png"),      
        pygame.image.load("Project stuff/Imagenes/ASCII_quit.png")
    ]
    def rec_imagenes(images):
        rec_list = []
        for i in images:
            rec_im = i.get_rect()
            rec_list.append(rec_im)
        return rec_list
    
    lista_rect = rec_imagenes(imagenes)

    #Funcion para cambiar color de matriz al apretarse.
    def cambio_matriz(mapa, mapa1): 
        global n
        pos_mouse = pygame.mouse.get_pos()
        matriz, coords = dibujar_matriz(mapa) 

        for rec in matriz:
            if rec.collidepoint(pos_mouse):
                
                i = matriz.index(rec)
                mapa = mapa1.Draw(mapa, n, coords[i])

                return mapa
        return mapa
        
    #Funcion para detectar click en boton
    def detectar_botones(botones):
        global n
        pos_mouse = pygame.mouse.get_pos()
        for i, boton in enumerate(botones):
            if boton.collidepoint(pos_mouse):
                n = i 
    
    #Crea botones en la pantalla
    def crear_botones_colores():
        botones = []
        x_start = 110  # Posición inicial x
        y = 70  # Posición fija y
        spacing = 70  # Espaciado entre botones
        
        for i in range(0,10):
            x = x_start + (i - 1) * spacing
            rec_base = pygame.Rect(x, y, 50, 50)    
            pygame.draw.rect(ventana,colors[i], rec_base)
            pygame.draw.rect(ventana, color_negro, rec_base, 1)
            botones.append(rec_base)

        return botones

    def dibujar_matriz(map):
        lista_matriz = [] #Lista con elementos de matriz
        cords_matriz = [] #Lista con coordenadas 
        cell_size = 40  # Tamaño de cada celda
        offset_x = 50  # Offset en x para centrar la matriz
        offset_y = 150  # Offset en y para centrar la matriz
        for row in range(12):
            for col in range(12):
                color = colors[map[row][col]]
                rec = pygame.draw.rect(ventana, color, pygame.Rect(col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size))
                pygame.draw.rect(ventana, color_negro, pygame.Rect(col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size), 1)
                cords_matriz.append([row, col])
                lista_matriz.append(rec)

        return lista_matriz, cords_matriz
    

    #Coloca imagenes verticales
    def colocar_imagenes(lista, images, rects):
        i = 0
        while i < 13:
            ventana.blit(images[i], (lista[i].centerx - rects[i].width // 2 , lista[i].centery - rects[i].height // 2 ))
            i += 1

    def mostrar_numeros(map, boleano):
        if boleano:
            color = (0,0,0)
        else:
            color = (214, 88, 180)

        lista_matriz = [] #Lista con elementos de matriz 
        cell_size = 20  # Tamaño de cada celda
        offset_x = 800  # Offset en x para centrar la matriz
        offset_y = 80  # Offset en y para centrar la matriz
        for row in range(12):
            for col in range(12):
                rec = pygame.draw.rect(ventana, (214, 88, 180), pygame.Rect(col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size))
                number_text = font.render(str(map[row][col]), True, color)
                text_rect = number_text.get_rect(center=rec.center)
                ventana.blit(number_text, text_rect)
                lista_matriz.append(rec)
                lista_matriz.append(rec)

        return lista_matriz
    def verifica_estado_matriz_num(boolean, mapa):
        if boolean:
            mostrar_numeros(mapa, estado_matriz_num)
        else:
            mostrar_numeros(mapa, estado_matriz_num)


    #Se deja mapa1 afuera de while para que se pueda modificar la lista mapa_base
    mapa1 = editor(direccion, nombre, "en proceso") 
    mapa_base = mapa1.cargar_matriz()
    estado_matriz_num = False
    running = True
    mouse_apretado = False


    while running:
        pygame.display.flip() #Actualizar pantalla
        
        pos_mouse = pygame.mouse.get_pos()

        for i in lista_botones:
            if i.collidepoint(pos_mouse):
                pygame.draw.rect(ventana, boton_color_encima, i)
            else:
                pygame.draw.rect(ventana,boton_color, i)


        #Mapa dentro de while para que se vaya actualizando
        dibujar_matriz(mapa_base)

        #Dibuja el borde de cada botón y coloca el texto correspondiente
        for boton, texto in botones_y_textos:
            pygame.draw.rect(ventana, color_negro, boton, 1)
            texto_rect = texto.get_rect(center=boton.center)
            ventana.blit(texto, texto_rect)

        for boton in lista_botones:
            pygame.draw.rect(ventana, color_negro, boton, 1)
        crear_botones_colores()
   
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_fin.collidepoint(pos_mouse):
                    running = False
                    escribir_matriz_en_txt(mapa_base, nombre + ".txt")
                    ventana_menu()
                elif boton_ver_matriz.collidepoint(pos_mouse):
                    estado_matriz_num = True
                    mostrar_numeros(mapa_base, estado_matriz_num)

                elif boton_hide_matriz.collidepoint(pos_mouse):
                    estado_matriz_num = False
                    mostrar_numeros(mapa_base, estado_matriz_num)

                elif boton_der.collidepoint(pos_mouse):
                    mapa_base = mapa1.rotar_derecha(mapa_base)
                    verifica_estado_matriz_num(estado_matriz_num, mapa_base)

                elif boton_izq.collidepoint(pos_mouse):
                    mapa_base = mapa1.rotar_izquierda(mapa_base)
                    verifica_estado_matriz_num(estado_matriz_num, mapa_base)
                
                elif boton_vert.collidepoint(pos_mouse):
                    mapa_base = mapa1.rotar_vertical(mapa_base)
                    verifica_estado_matriz_num(estado_matriz_num, mapa_base)

                elif boton_hor.collidepoint(pos_mouse):
                    mapa_base = mapa1.rotar_horizontal(mapa_base)
                    verifica_estado_matriz_num(estado_matriz_num, mapa_base)
                
                elif boton_neg.collidepoint(pos_mouse):
                    mapa_base = mapa1.negativo(mapa_base)
                    verifica_estado_matriz_num(estado_matriz_num, mapa_base)
                
                elif boton_romb.collidepoint(pos_mouse):
                    mapa_base = mapa1.rombo(mapa_base, n)
                    verifica_estado_matriz_num(estado_matriz_num, mapa_base)
                
                elif boton_cuadr.collidepoint(pos_mouse):
                    mapa_base = mapa1.cuadrado(mapa_base ,n)
                    verifica_estado_matriz_num(estado_matriz_num, mapa_base)

                if event.button == 1:  
                    mouse_apretado = True
                    botones = crear_botones_colores()
                    detectar_botones(botones)
                    mapa_base = cambio_matriz(mapa_base, mapa1)
                    verifica_estado_matriz_num(estado_matriz_num, mapa_base)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    mouse_apretado = False

        if mouse_apretado:
            botones = crear_botones_colores()
            detectar_botones(botones)
            mapa_base = cambio_matriz(mapa_base, mapa1)
            verifica_estado_matriz_num(estado_matriz_num, mapa_base)
        
        colocar_imagenes(lista_botones_con_imagenes, imagenes, lista_rect)

#______________________________________________Inicio pygame____________________________________________________________
#Inicio pygame
pygame.init()

#Llamada ventana de menu
ventana_menu()