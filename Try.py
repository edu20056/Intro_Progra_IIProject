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

APPWIDTH = int(get_monitors()[0].width * 0.90)
APPHEIGHT = int(get_monitors()[0].height * 0.85)

FPS = 60

colors = {
    0: (255, 255, 255),  
    1: (104, 95, 109), 
    2: (0, 255, 0),  
    3: (248, 12, 12), 
    4: (237, 248, 12),
    5: (12, 237, 248),
    6: (12, 41, 248), 
    7: (151, 9, 242), 
    8: (253, 19, 168),
    9: (0, 0, 0),  
}

codif = {
    0: " ",
    1: ".",
    2: ":",
    3: "-",
    4: "=",
    5: "¡",
    6: "&",
    7: "$",
    8: "%",
    9: "@"
}

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

class Canvas:

    def __init__(self, archivo):

        if archivo:
            self.archivo = archivo
            self.estado = "en proceso"
            self.nombre = os.path.basename(self.archivo)
        else:
            self.estado = "sin guardar"
            self.nombre = "Nuevo Lienzo"

        self.matrix = []
        with open(self.archivo, 'r') as file:
            txt_lines = file.readlines()
            for line in txt_lines:
                row = list(map(int, line.strip().split()))
                if row:
                    self.matrix.append(row)
        file.close()

    def ClockWise(self, matrix):

        res = []
        lista_aux = []

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                lista_aux.append(matrix[j][i])
            res.append(lista_aux[::-1])
            lista_aux = []
        
        return res

    def Anti_ClockWise(self, result):

        res = []
        filas = len(result)
        columnas = len(result[0])

        for i in range(len(result)):
            nueva_fila = []
            for j in range(filas):
                nueva_fila.append(result[j][columnas - 1 - i])
            res.append(nueva_fila)

        return res
    
    def Mirror_hrz(self, matrix):
    
        res = []
        for i in matrix:
            res.append(i[::-1])
        return res

    def Mirror_vrt(self, matrix):
    
        pos = len(matrix) -1
        result = []
        while 0 <= pos:
            result.append(matrix[pos])
            pos -= 1
        return result
    
    def Draw(self, matrix, color, coords) :

        row, col = coords
        matrix[row][col] = color
        return matrix 
    
    def Negative(self, matrix):

        res = []
        lista_aux = []

        for i in matrix:
            for j in i:
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
                
                if j < 5:
                    x = 0
                else:
                    x = 9

                lista_aux.append(x)
            res.append(lista_aux)
            lista_aux = []
        
        return res

    def Square(self, matrix, color):
        
        square_size = len(matrix) // 2
        n = len(matrix)

        start = (n - square_size) // 2
        end = start + square_size

        for i in range(start, end):
            for j in range(start, end):

                if i == start or i == end - 1:
                    matrix[i][j] = color

                elif j == start or j == end - 1:
                    matrix[i][j] = color
        return matrix

    def Rhomb(self, matrix, color):

        n = len(matrix)
        center = n // 2
        
        for i in range(n):
            for j in range(n):
                if abs(center - i) + abs(center - j) == len(matrix) // 2 - 1 :
                    matrix[i][j] = color
        return matrix

class Button:

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
        
        self.color = self.color_off
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.color = self.color_on

    def Display(self, screen):
        
        self.Over()

        self.surface.fill(self.color)

        if self.photo:
            screen.blit(self.surface, self.rect)
            image = pygame.image.load(self.photo)
            scaled_image = pygame.transform.scale(image, self.size)
            image_rect = scaled_image.get_rect(center=self.rect.center)
            screen.blit(scaled_image, image_rect.topleft)
        else:
            self.surface.blit(self.text_surface, self.text_rect)
            screen.blit(self.surface, self.rect)
    
    def Exe(self, *args):
        if self.command:
            return self.command(*args)

class Editor:

    def __init__(self, path= None, font= ("Times New Roman", 14), edge= True):
    
        self.width = APPWIDTH
        self.height = APPHEIGHT

        if path:
            self.path = path
            self.status = "In progress"
            self.name = os.path.basename(self.path)
        else:
            self.path = "Draft.txt"
            self.status = "Not saved"
            self.name = "New Proyect"

        self.Canvas = Canvas(self.path)
        self.matrix = self.Canvas.matrix
        self.save = copy.deepcopy(self.Canvas.matrix)

        self.zoom_index = 1.0
        self.brush = 0
        self.edge = edge

        pygame.init()
        pygame.display.set_icon(pygame.image.load("Images/logo.png"))
        self.font = pygame.font.SysFont(font[0], font[1])
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"{self.name} [{len(self.matrix)}x{len(self.matrix)}] - ({self.status})")

        self.canvas_surface = pygame.Surface((int(self.width * 0.90), self.height))
        self.canvas_surface.fill((30, 30, 30))

        self.colorMenu_surface = pygame.Surface((int(self.width * 0.05), int(self.height * 0.75)))
        self.colorMenu_surface.fill((48, 48, 48))

        self.optsMenu_surface = pygame.Surface((int(self.width * 0.15), self.height))
        self.optsMenu_surface.fill((48, 48, 48))

    def Grid(self, grid):

        list_matrix = []
        coords_matrix = [] 
        cell_size = self.canvas_surface.get_height() // len(self.matrix)
        
        for row in range(len(grid)):
            for col in range(len(grid[0])):

                color = colors[grid[row][col]]
                left = (col * cell_size) + (self.canvas_surface.get_width() - len(self.matrix[0]) * cell_size) // 2
                top = (row * cell_size) + (self.canvas_surface.get_height() - len(self.matrix) * cell_size) // 2

                rec = pygame.draw.rect(self.canvas_surface, color, pygame.Rect(left, top, cell_size, cell_size))
                
                if self.edge:
                    pygame.draw.rect(self.canvas_surface, (150, 150, 150), pygame.Rect(left, top, cell_size, cell_size), 1)
                
                coords_matrix.append([row, col])
                list_matrix.append(rec)

        return list_matrix, coords_matrix

    def Zoom(self, surface, zoom_factor):

        width = int(surface.get_width() * zoom_factor)
        height = int(surface.get_height() * zoom_factor)
        return pygame.transform.scale(surface, (width, height))
    
    def ColorMenu(self, surface):

        button_list = []
        radius = int(surface.get_width() * 0.20)
        y_start = int(surface.get_height() * 0.065)
        x = int(surface.get_width() // 2)
        spacing = int(surface.get_height() * 0.10)

        for j in range(len(colors)):

            y = y_start + j * spacing
            center = (x, y)
            rec_base = pygame.Rect(0, j * surface.get_height() // 10 + surface.get_height() * 0.195, surface.get_width(), surface.get_height() // 10) 
            pygame.draw.circle(surface, colors[j], center, radius)
            button_list.append(rec_base)

        return button_list

    def Paint(self, plane, canvas, canvas_rect):

        pos_mouse = pygame.mouse.get_pos()
        pos_mouse_adj = ((pos_mouse[0] - canvas_rect.left) / self.zoom_index, (pos_mouse[1] - canvas_rect.top) / self.zoom_index)
        matrix, coords = self.Grid(plane) 

        for rec in matrix:
            if rec.collidepoint(pos_mouse_adj):
                i = matrix.index(rec)
                plane = canvas.Draw(plane, self.brush, coords[i])
                return plane
        return plane

    def PrintCore(self, core, encode):

        display = tk.Tk()
        display.title(f"{self.name} [{len(self.matrix)}x{len(self.matrix)}] - Core ")
        display.iconbitmap("Images/icon.ico")
        display.config(background= "white")

        canvas = tk.Canvas(display, background= "white")
        canvas.pack(side="left", fill="both", expand=True)

        y_scrollbar = tk.Scrollbar(display, orient="vertical", command=canvas.yview)
        y_scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=y_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        frame = tk.Frame(canvas, background= "white")
        canvas.create_window((display.winfo_width() // 2, display.winfo_height() // 2), window=frame, anchor="center")

        for i, row in enumerate(core):
            for j, val in enumerate(row):
                cell_font = ("Times New Roman", 16, "bold")

                if encode:
                    element = codif[val]
                else:
                    element = str(val)

                cell = tk.Label(frame, text= element, font=cell_font, borderwidth= 0, relief= "solid", width= 1, height= 1, fg= "black", background= "white")
                cell.grid(row= i, column= j, padx= 5, pady= 5)

        display.mainloop()
    
    def OpenFile(self): 

        file_path = askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            pygame.quit()
            Editor(path= file_path).Exe()

    def SaveFile(self):

        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            with open(file_path, 'w') as file:
                lines = [" ".join(map(str, row)) for i, row in enumerate(self.matrix)]
                content = "\n".join(lines)
                file.write(content)

            self.path = file_path
            self.status = "In progress"
            self.name = os.path.basename(self.path)
            pygame.display.set_caption(f"{self.name} [{len(self.matrix)}x{len(self.matrix)}] - ({self.status})")
                
            file.close()

    def Exe(self):
        
        canvas_x = self.canvas_surface.get_width() // 2
        canvas_y = self.canvas_surface.get_height() // 2

        button_size = int(self.optsMenu_surface.get_width() * 0.15)
        
        highContrs = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.925, APPHEIGHT * 0.25), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/highContrast.png")
        negative = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.75, APPHEIGHT * 0.25), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/negative.png")
        
        edge_b = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.585), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/edge.png")
        see_matrix = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.635), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/display.png")
        see_ascii = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.685), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/display.png")

        shape_squrd = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.60, APPHEIGHT * 0.80), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/square.png")
        shape_diam = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.80), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/rombo.png")

        turnRight = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.20, APPHEIGHT * 0.90), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/right.png")
        turnLeft = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.80, APPHEIGHT * 0.90), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/left.png")
        mirrorVert = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.60, APPHEIGHT * 0.90), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/mirrorV.png")
        mirrorHorz = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.40, APPHEIGHT * 0.90), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/mirrorH.png")

        return_b = Button(coords=(APPWIDTH - self.optsMenu_surface.get_width() * 0.125, APPHEIGHT * 0.25), size= (button_size, button_size), up= [48, 48, 48], down= [30, 30, 30], photo= "Images/return.png")

        button_list = [turnRight, turnLeft, mirrorVert, mirrorHorz, highContrs, negative, edge_b, shape_squrd, shape_diam, see_matrix, see_ascii, return_b]

        running = True
        while running:

            self.screen.fill((30, 30, 30))

            self.Grid(self.matrix)

            scaled_canvas = self.Zoom(self.canvas_surface, self.zoom_index)
            canvas_rect = scaled_canvas.get_rect(center=(canvas_x, canvas_y))
            self.screen.blit(scaled_canvas, canvas_rect)

            clrs = self.ColorMenu(self.colorMenu_surface)

            self.screen.blit(self.colorMenu_surface, (0, int(self.height * 0.25) // 2))

            sample = pygame.Rect(0, int(self.optsMenu_surface.get_height() * 0.075), self.optsMenu_surface.get_width(), int(self.optsMenu_surface.get_height() * 0.15) )    
            pygame.draw.rect(self.optsMenu_surface, colors[self.brush], sample)
            self.screen.blit(self.optsMenu_surface, (int(self.width * 0.85), 0))

            color_title = self.font.render(f"{colors[self.brush]}", True, (255, 255, 255))
            color_title_rect = color_title.get_rect(topright=(self.screen.get_width() - 5, APPHEIGHT * 0.035))
            self.screen.blit(color_title, color_title_rect)

            edge_title = self.font.render("EDGES", True, (255, 255, 255))
            edge_title_rect = edge_title.get_rect(topleft=(APPWIDTH * 0.875, APPHEIGHT * 0.575))
            self.screen.blit(edge_title, edge_title_rect)

            normal_title = self.font.render("NOR.M.D.", True, (255, 255, 255))
            normal_title_rect = normal_title.get_rect(topleft=(APPWIDTH * 0.875, APPHEIGHT * 0.625))
            self.screen.blit(normal_title, normal_title_rect)

            ascii_title = self.font.render("A.S.C.I.I.", True, (255, 255, 255))
            ascii_title_rect = ascii_title.get_rect(topleft=(APPWIDTH * 0.875, APPHEIGHT * 0.675))
            self.screen.blit(ascii_title, ascii_title_rect)

            shapes_title = self.font.render("SHAPES", True, (255, 255, 255))
            shapes_title_rect = shapes_title.get_rect(topleft=(APPWIDTH * 0.875, APPHEIGHT * 0.745))
            self.screen.blit(shapes_title, shapes_title_rect)

            for b in button_list:
                b.Display(self.screen)

            pos_mouse = pygame.mouse.get_pos()

            if self.colorMenu_surface.get_width() < pygame.mouse.get_pos()[0] < int(APPWIDTH * 0.80):
                pygame.mouse.set_visible(False)
                brush_size = self.canvas_surface.get_height() // (2 * len(self.matrix)) * self.zoom_index
                pygame.draw.circle(self.screen, colors[self.brush], pos_mouse, brush_size, 3)
            else:
                pygame.mouse.set_visible(True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
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

                    if event.key in key_mapping:
                        current_value = key_mapping[event.key]
                        self.brush = current_value

                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        
                        if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                            if self.zoom_index < 1.6:
                                self.zoom_index += 0.1
                        
                        elif event.key == pygame.K_MINUS:
                            if self.zoom_index > 0.4:
                                self.zoom_index -= 0.1
                        
                        elif event.key == pygame.K_z:
                            self.matrix = copy.deepcopy(self.save)

                        elif event.key == pygame.K_s:
                            self.SaveFile()

                        elif event.key == pygame.K_o:
                            self.OpenFile()
                        
                        elif event.key == pygame.K_SPACE:
                            self.matrix = [[0 for _ in row] for row in self.matrix]

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        for color, button in enumerate(clrs):
                            if button.collidepoint(pos_mouse):
                                self.brush = color  

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
                                    self.matrix = self.Canvas.Square(self.matrix, self.brush)
                                elif b == shape_diam:
                                    self.matrix = self.Canvas.Rhomb(self.matrix, self.brush)
                                elif b == see_matrix:
                                    self.PrintCore(self.matrix, False)
                                elif b == see_ascii:
                                    self.PrintCore(self.matrix, True)
                                elif b == edge_b:
                                    self.edge = not self.edge
                                elif b == return_b:
                                    self.matrix = copy.deepcopy(self.save)
                    
                    if event.button == 3:
                        self.brush = 0

                    if event.button == 4:
                        if self.zoom_index < 1.6:
                            self.zoom_index += 0.1
                    
                    elif event.button == 5:
                        if self.zoom_index > 0.4:
                            self.zoom_index -= 0.1

            if pygame.mouse.get_pressed()[0]:
                self.matrix = self.Paint(self.matrix, self.Canvas, canvas_rect)
                                    
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == '__main__':

    Editor().Exe()