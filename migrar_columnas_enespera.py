import sqlite3

db_path = "hospitrack.db"  # Asegúrate que el archivo esté en el mismo directorio
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def agregar_columna_si_falta(nombre_columna, tipo_sqlite):
    try:
        cursor.execute(f"ALTER TABLE dsoftware_enespera ADD COLUMN {nombre_columna} {tipo_sqlite};")
        print(f"✅ Columna '{nombre_columna}' agregada.")
    except sqlite3.OperationalError as e:
        if f"duplicate column name: {nombre_columna}" in str(e):
            print(f"✔️ Columna '{nombre_columna}' ya existe.")
        else:
            print(f"⚠️ Error con columna '{nombre_columna}': {e}")

# Agregar las columnas necesarias
agregar_columna_si_falta("Comentario", "TEXT")
agregar_columna_si_falta("EstadoFinal", "TEXT")
agregar_columna_si_falta("FechaResolucion", "TEXT")

conn.commit()
conn.close()
print("Migración finalizada.")
