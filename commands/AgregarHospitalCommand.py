# Este archivo define un comando específico que encapsula la acción de agregar un hospital.
# Implementa el patrón de diseño Command (patrón de comportamiento).

class AgregarHospitalCommand:
    def __init__(self, fachada, nombre, lat, lon):
        """
        Constructor del comando.
        :param fachada: instancia de AdminHospitalFacade
        :param nombre: nombre del hospital
        :param lat: latitud del hospital (float)
        :param lon: longitud del hospital (float)
        """
        self.fachada = fachada
        self.nombre = nombre
        self.lat = lat
        self.lon = lon

    def ejecutar(self):
        """
        Método principal del comando. Ejecuta la acción de agregar hospital usando la fachada.
        """
        self.fachada.agregar(self.nombre, self.lat, self.lon)
 