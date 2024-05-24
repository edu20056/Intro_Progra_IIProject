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


