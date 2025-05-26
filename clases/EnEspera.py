class EnEspera:
    def __init__(self, id:int, rut:str, prioridad:int, hora_registro:str):
        self.__id = id
        self.__rut = rut
        self.__prioridad = prioridad
        self.__hora_registro = hora_registro
    
    @property
    def id(self):
        return self.__id

    @property
    def rut(self):
        return self.__rut

    @property
    def prioridad(self):
        return self.__prioridad

    @property
    def hora_registro(self):
        return self.__hora_registro

    # Despues de ser creado el objeto no debería ser necesario modificarlo