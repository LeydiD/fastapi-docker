from fastapi import FastAPI, Request
import json
import os
import psycopg2
from app.database import Nota, SessionLocal, init_db
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()
init_db()

class NotaCreate(BaseModel):
    title: str
    content: str

@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }

# Este metodo devuelve las notas guardadas en la base de datos
@app.get("/notes")
def get_notes():
    try:
        db = SessionLocal()
        notas = db.query(Nota).all()
        return {"notes": [{"id": n.id, "title": n.title, "content": n.content} for n in notas]}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudo acceder a las notas")


@app.post("/notes")
async def create_note(nota: NotaCreate):
    try:
        db = SessionLocal()
        nueva_nota = Nota(title=nota.title, content=nota.content)
        db.add(nueva_nota)
        db.commit()
        db.refresh(nueva_nota)
        return {
            "message": "Nota guardada exitosamente",
            "note": {
                "id": nueva_nota.id,
                "title": nueva_nota.title,
                "content": nueva_nota.content
            }
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error de base de datos")