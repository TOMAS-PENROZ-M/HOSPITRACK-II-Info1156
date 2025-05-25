from datetime import datetime
class Seccion:
    def __init__(self, id:int, nombre:str, centrosalud:'CentroSalud', recepcionista:'Recepcionista'):
        self.__id = id
        self.__nombre = nombre
        self.__centrosalud = centrosalud
        self.__recepcionista = recepcionista
        self.__filaespera = []
        self.__solicitudes = []

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def centrosalud(self):
        return self.__centrosalud

    @property
    def recepcionista(self):
        return self.__recepcionista

    @property
    def filaespera(self):
        return self.__filaespera

    @property
    def solicitudes(self):
        return self.__solicitudes

    # Setters
    @nombre.setter
    def nombre(self, nombre:str):
        self.__nombre = nombre

    @centrosalud.setter
    def centrosalud(self, centrosalud:'CentroSalud'):
        self.__centrosalud = centrosalud

    @recepcionista.setter
    def recepcionista(self, recepcionista:'Recepcionista'):
        self.__recepcionista = recepcionista

    # Gestion de fila de espera
    # agregar con el objeto EnEspera ya hecho
    def agregar_en_espera(self, en_espera:'EnEspera'):
        self.__filaespera.append(en_espera)
    
    def agregar_a_fila(self,id:int, rut:str, prioridad:int):
        hora_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__filaespera.append(EnEspera(id, rut, prioridad, hora_registro))
    
    def eliminar_de_fila(self, id:int):
        for en_espera in self.__filaespera:
            if en_espera.id == id:
                self.__filaespera.remove(en_espera)
                break
    
    def longitud_fila(self):
        return len(self.__filaespera)
    
    # Gestion de solicitudes

    # wip