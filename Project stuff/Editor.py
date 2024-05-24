#Clase para listas

class editor:
    def __init__(self, txt, creator, state ):
        self.txt = txt
        self.creator = creator
        self.state = state
        
    #Método para cargar dibujo 
    def cargar_matriz(self):
        with open(self.txt, "r") as file:
            result = []
            for line in file:
                # Eliminar corchetes y espacios, luego dividir por comas
                line = line.strip().replace('[', '').replace(']', '').replace(' ', '')
                if line:
                    # Convertir cada elemento en entero y agregar a la lista resultante
                    row = list(map(int, line.split(',')))
                    result.append(row)
        return result
    
    #Métodos para rotar dibujo
    def rotar_derecha(self, result):
        res = []
        lista_aux = []
        for i in range(len(result)):
            for j in range(len(result[0])):
                lista_aux.append(result[j][i])
            res.append(lista_aux[::-1])
            lista_aux = []
        return res

    def rotar_izquierda(self, result):
        res = []
        filas = len(result)
        columnas = len(result[0])
        for i in range(len(result)):
            nueva_fila = []
            for j in range(filas):
                nueva_fila.append(result[j][columnas - 1 - i])
            res.append(nueva_fila)
        return res
    
    def rotar_horizontal(self, matriz):
        pos = len(matriz) -1
        result = []
        while 0 <= pos:
            result.append(matriz[pos])
            pos -= 1
        return result
    
    def rotar_vertical(self, matriz):
        res = []
        for i in matriz:
            res.append(i[::-1])
        return res
    
    #Método para modificar dibujo
    def Draw(self, matrix, color, coords) :
        row, col = coords
        matrix[row][col] = color
        return matrix 
    
    #Método para hacer negativo. 
    def negativo(self, matriz):
        res = []
        lista_aux = []
        for i in matriz:
            for j in i:
                x = 9 - j
                lista_aux.append(x)
            res.append(lista_aux)
            lista_aux = []
        return res
    
    #Método para cuadrado y rombo.
    def cuadrado(self, matriz, color):
        for i in range(len(matriz)):
            if i in [2, 9]:
                for j in range(2, 10):
                    matriz[i][j] = color
            elif i not in [0,1,10,11]:
                matriz[i][2] = color
                matriz[i][9] = color
        return matriz

    def rombo(self, matriz, color):
        for i in range(len(matriz)):
            if i in [0,11]:
                matriz[i][5] = color
                matriz[i][6] = color
            elif i in [1,10]:
                matriz[i][4] = color
                matriz[i][7] = color
            elif i in [2,9]:
                matriz[i][3] = color
                matriz[i][8] = color
            elif i in [3,8]:
                matriz[i][2] = color
                matriz[i][9] = color
            elif i in [4,7]:
                matriz[i][1] = color
                matriz[i][10] = color
            else:
                matriz[i][0] = color
                matriz[i][11] = color
        return matriz

