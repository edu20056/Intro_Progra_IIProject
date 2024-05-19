#Clase para listas

class editor:
    def __init__(self, txt, creator, state ):
        self.txt = txt
        self.creator = creator
        self.state = state

    def matriz(self):
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
    def transpuesta(self):
        with open(self.txt, "r") as file:
            result = []
            for line in file:
                # Eliminar corchetes y espacios, luego dividir por comas
                line = line.strip().replace('[', '').replace(']', '').replace(' ', '')
                if line:
                    # Convertir cada elemento en entero y agregar a la lista resultante
                    row = list(map(int, line.split(',')))
                    result.append(row)
        file.close()
        res = []
        lista_aux = []
        for i in range(len(result)):
            for j in range(len(result[0])):
                lista_aux.append(result[j][i])
            res.append(lista_aux)
            lista_aux = []
        return res