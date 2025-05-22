import sys
import os

# Usar la ruta raiz del proyecto para importar las clases
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.CentroSalud import CentroSalud
from clases.Seccion import Seccion
from clases.EnEspera import EnEspera

from database import get_db
from models import CentroSaludDB, SeccionDB, EnEsperaDB

class Marker:
    def __init__(self, centro_salud: CentroSalud, marker_id: int):
        self.centro_salud = centro_salud
        self.marker_id = marker_id
        self.is_selected = False

class Mapa:
    def __init__(self, widget:'tkintermapview.TkinterMapView'):
        self.__widget = widget
        self.__markers = []
        self.__selected_marker = None

    @property
    def widget(self):
        return self.__widget

    @property
    def markers(self):
        return self.__markers
    
    @property
    def selected_marker(self):
        return self.__selected_marker

    # Obtener centros de salud de la base de datos, incluyendo secciones y listas de espera de cada seccion
    def obtener_centros_salud(self):
        sesion = next(get_db())
        with sesion as session:
            centros_salud_db = session.query(CentroSaludDB).all()
            for centro_db in centros_salud_db:
                centro = CentroSalud(centro_db.IdCentro, centro_db.Nombre, centro_db.Latitud, centro_db.Longitud)
                secciones_db = session.query(SeccionDB).filter(SeccionDB.IdCentro == centro_db.IdCentro).all()
                for seccion_db in secciones_db:
                    seccion = Seccion(seccion_db.IdSeccion, seccion_db.NombreSeccion, centro_db, None)
                    en_espera = []
                    en_espera_db = session.query(EnEsperaDB).filter(EnEsperaDB.IdSeccion == seccion_db.IdSeccion).all()
                    for en_espera_db_item in en_espera_db:
                        en_espera.append(EnEspera(en_espera_db_item.IdRegistro, en_espera_db_item.RUT, en_espera_db_item.Prioridad, en_espera_db_item.HoraRegistro))
                    seccion.agregar_en_espera(en_espera)
                    centro.agregar_seccion(seccion)
                marker = Marker(centro, centro.id)
                self.__markers.append(marker)
    
    def mostrar_centros(self):
        if len(self.__markers) > 0:
            print("Se han encontrado los siguientes centros de salud:")
            for marker in self.__markers:
                print(f"Centro de Salud: {marker.centro_salud.nombre}, Latitud: {marker.centro_salud.latitud}, Longitud: {marker.centro_salud.longitud}")
        else:
            print("No se han encontrado centros de salud.")

    def update_map(self):
        self.__widget.delete_all_marker()
        for marker in self.__markers:
            centro = marker.centro_salud
            self.__widget.add_marker(
                lat=centro.latitud,
                lng=centro.longitud,
                title=centro.nombre,
                marker_id=marker.marker_id
            )

    def select_marker(self, marker_id):
        for marker in self.__markers:
            if marker.marker_id == marker_id:
                marker.is_selected = True
                self.__selected_marker = marker
            else:
                marker.is_selected = False