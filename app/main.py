from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.responses import FileResponse
import os

app = FastAPI()

# 🔐 senha segura (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🧠 banco em memória (fake DB)
users_db = {}
user_id_counter = 1


# =========================
# MODELOS
# =========================
class UserCreate(BaseModel):
    username: str
    password: str


class LoginData(BaseModel):
    username: str
    password: str


# =========================
# FRONTEND
# =========================
@app.get("/")
def home():
    file_path = os.path.join("frontend", "index.html")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="frontend não encontrado")

    return FileResponse(file_path)


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# CREATE USER
# =========================
@app.post("/users")
def create_user(user: UserCreate):
    global user_id_counter

    # evita usuário duplicado
    for u in users_db.values():
        if u["username"] == user.username:
            raise HTTPException(status_code=409, detail="usuário já existe")

    hashed_password = pwd_context.hash(user.password)

    users_db[user_id_counter] = {
        "id": user_id_counter,
        "username": user.username,
        "password_hash": hashed_password
    }

    user_id_counter += 1

    return {
        "id": user_id_counter - 1,
        "username": user.username
    }


# =========================
# LISTAR USUÁRIOS (NOVO)
# =========================
@app.get("/users")
def list_users():
    return [
        {"id": u["id"], "username": u["username"]}
        for u in users_db.values()
    ]


# =========================
# LOGIN
# =========================
@app.post("/login")
def login(data: LoginData):

    for user in users_db.values():
        if user["username"] == data.username:
            if pwd_context.verify(data.password, user["password_hash"]):
                return {
                    "message": "login ok",
                    "user_id": user["id"],
                    "username": user["username"]
                }

    raise HTTPException(status_code=401, detail="usuário ou senha inválidos")


# =========================
# UPDATE PASSWORD
# =========================
@app.put("/users/{user_id}/password")
def update_password(user_id: int, data: LoginData):

    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="usuário não encontrado")

    users_db[user_id]["password_hash"] = pwd_context.hash(data.password)

    return {"message": "senha atualizada"}


# =========================
# DELETE USER
# =========================
@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="usuário não encontrado")

    del users_db[user_id]

    return {"message": "usuário deletado"}

    # teste pipeline