from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection
from datetime import datetime, timedelta

app = FastAPI(title="Venus API")

# -------------------------
# MODELOS
# -------------------------
class Usuario(BaseModel):
    nombre: str
    apellido: str
    correo: str
    contrasena: str


class Ciclo(BaseModel):
    id_usuario: int
    fecha_inicio: str
    duracion_ciclo: int


class Login(BaseModel):
    correo: str
    contrasena: str


# -------------------------
# HOME
# -------------------------
@app.get("/")
def home():
    return {"message": "Venus API funcionando"}

# -------------------------
# USUARIOS
# -------------------------
@app.get("/usuarios")
def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuario")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.post("/usuarios")
def create_usuario(usuario: Usuario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuario (nombre, apellido, correo, contrasena)
        VALUES (?, ?, ?, ?)
    """, (
        usuario.nombre,
        usuario.apellido,
        usuario.correo,
        usuario.contrasena
    ))

    conn.commit()
    conn.close()

    return {"message": "Usuario creado correctamente"}


# -------------------------
# LOGIN (NUEVO)
# -------------------------
@app.post("/login")
def login(data: Login):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuario
        WHERE correo = ? AND contrasena = ?
    """, (data.correo, data.contrasena))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"message": "Credenciales incorrectas"}

    return {
        "message": "Login exitoso",
        "usuario": dict(user)
    }


# -------------------------
# CICLOS
# -------------------------
@app.get("/ciclos/historial/{id_usuario}")
def historial_ciclos(id_usuario: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM ciclo_menstrual
        WHERE id_usuario = ?
        ORDER BY id_ciclo DESC
    """, (id_usuario,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/ciclos/fases/{id_usuario}")
def fases_usuario(id_usuario: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT fecha_inicio, fecha_ovulacion, fecha_fin
        FROM ciclo_menstrual
        WHERE id_usuario = ?
        ORDER BY id_ciclo DESC
        LIMIT 1
    """, (id_usuario,))

    ciclo = cursor.fetchone()
    conn.close()

    if not ciclo:
        return {"message": "No hay ciclos registrados"}

    return {
        "fase_menstrual": ciclo["fecha_inicio"],
        "fase_ovulacion": ciclo["fecha_ovulacion"],
        "fin_ciclo": ciclo["fecha_fin"]
    }


# -------------------------
# DELETE USUARIO
# -------------------------
@app.delete("/usuarios/{id_usuario}")
def delete_usuario(id_usuario: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))

    conn.commit()
    conn.close()

    return {"message": "Usuario eliminado"}