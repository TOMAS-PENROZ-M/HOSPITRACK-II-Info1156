class CentroSalud:
    def __init__(self, id:int, nombre:str, latitud:float, longitud:float):
        self.__id = id
        self.__nombre = nombre
        self.__latitud = latitud
        self.__longitud = longitud
        self.__secciones = []

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def latitud(self):
        return self.__latitud

    @property
    def longitud(self):
        return self.__longitud

    @property
    def secciones(self):
        return self.__secciones
    
    # Setters
    @nombre.setter
    def nombre(self, nombre:str):
        self.__nombre = nombre

    @latitud.setter
    def latitud(self, latitud:float):
        self.__latitud = latitud

    @longitud.setter
    def longitud(self, longitud:float):
        self.__longitud = longitud

    # Gestion de secciones
    def agregar_seccion(self, seccion:'Seccion'):
        self.__secciones.append(seccion)

    def eliminar_seccion(self, seccion:'Seccion'):
        self.__secciones.remove(seccion)
