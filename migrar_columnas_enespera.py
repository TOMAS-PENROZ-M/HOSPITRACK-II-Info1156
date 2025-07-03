import sqlite3
from datetime import datetime

db_path = "hospitrack.db"  # Asegúrate que el archivo esté en el mismo directorio
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def agregar_columna_si_falta(tabla, nombre_columna, tipo_sqlite, valor_por_defecto=None):
    try:
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {nombre_columna} {tipo_sqlite};")
        print(f"✅ Columna '{nombre_columna}' agregada a la tabla '{tabla}'.")
        if valor_por_defecto is not None:
            cursor.execute(f"UPDATE {tabla} SET {nombre_columna} = ? WHERE {nombre_columna} IS NULL;", (valor_por_defecto,))
            print(f"✅ Valor por defecto '{valor_por_defecto}' asignado a la columna '{nombre_columna}'.")
    except sqlite3.OperationalError as e:
        if f"duplicate column name: {nombre_columna}" in str(e):
            print(f"✔️ Columna '{nombre_columna}' ya existe en la tabla '{tabla}'.")
        else:
            print(f"⚠️ Error con columna '{nombre_columna}' en la tabla '{tabla}': {e}")

# Agregar las columnas necesarias
agregar_columna_si_falta("dsoftware_solicitud", "prioridad", "TEXT", "Media")
agregar_columna_si_falta("dsoftware_solicitud", "Tipo", "TEXT", "N/A")  # Nueva columna Tipo
agregar_columna_si_falta("dsoftware_enespera", "Comentario", "TEXT")
agregar_columna_si_falta("dsoftware_enespera", "EstadoFinal", "TEXT")
agregar_columna_si_falta("dsoftware_enespera", "FechaResolucion", "TEXT", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
agregar_columna_si_falta("dsoftware_enespera", "Tipo", "TEXT", "N/A")
agregar_columna_si_falta("dsoftware_enespera", "TurnoAsignado", "TEXT", "")

# Confirmar cambios
conn.commit()
conn.close()
print("Migración finalizada.")