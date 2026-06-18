import sqlite3

print("Iniciando creación de base de datos...")

conn = sqlite3.connect("venus.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    apellido TEXT,
    correo TEXT,
    contrasena TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ciclo_menstrual (
    id_ciclo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    fecha_inicio TEXT,
    duracion_ciclo INTEGER,
    fecha_ovulacion TEXT,
    fecha_fin TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cita_medica (
    id_cita INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    especialidad TEXT,
    fecha_cita TEXT,
    hora_cita TEXT,
    observaciones TEXT
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente ✔")