# 3. recepcionista/patrones/exportador.py
from abc import ABC, abstractmethod

class IExportStrategy(ABC):
    @abstractmethod
    def exportar(self, records: list, path: str): pass

class ExportadorCSV(IExportStrategy):
    def exportar(self, records: list, path: str):
        import csv
        if not records: return
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(records[0].__dict__.keys())
            for rec in records:
                writer.writerow(rec.__dict__.values())

class ExportadorPDF(IExportStrategy):
    def exportar(self, records: list, path: str):
        from reportlab.platypus import SimpleDocTemplate, Table
        if not records: return
        data = [list(records[0].__dict__.keys())] + [list(r.__dict__.values()) for r in records]
        doc = SimpleDocTemplate(path)
        table = Table(data)
        doc.build([table])

