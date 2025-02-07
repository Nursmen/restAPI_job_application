from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import TypeCreate, TypeResponse

router = APIRouter()

@router.post("/types", response_model=TypeResponse)
def create_type(type_data: TypeCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Type (name) VALUES (?)", (type_data.name,))
    db.commit()
    return {"id": cursor.lastrowid, "name": type_data.name}

@router.get("/types", response_model=list[TypeResponse])
def get_types(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Type")
    return [dict(row) for row in cursor.fetchall()]