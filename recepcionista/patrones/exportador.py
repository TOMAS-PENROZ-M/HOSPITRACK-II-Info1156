from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

class Exportador(ABC):
    @abstractmethod
    def exportar(self, datos):
        pass

class ExportadorPDF(Exportador):
    def __init__(self, archivo):
        self.archivo = archivo

    def exportar(self, registros):
        c = canvas.Canvas(self.archivo, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height-50, "Historial de Atenciones")
        c.setFont("Helvetica", 10)
        c.drawString(50, height-70, f"Total registros: {len(registros)}")
        y = height - 100
        headers = ["ID","RUT","Sección","Prioridad","Estado","Comentario","Fecha"]
        c.setFont("Helvetica-Bold", 10)
        for i, h in enumerate(headers):
            c.drawString(50 + i*80, y, h)
        y -= 20
        c.setFont("Helvetica", 9)
        for rec in registros:
            fila = [
                str(rec.IdRegistro), rec.RUT or '', str(rec.IdSeccion), rec.Prioridad or '',
                rec.EstadoFinal or '', (rec.Comentario or '')[:30],
                rec.FechaResolucion.strftime("%Y-%m-%d") if rec.FechaResolucion else ''
            ]
            for i, val in enumerate(fila):
                c.drawString(50 + i*80, y, val)
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50
        c.save()