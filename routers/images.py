from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from database import get_db
from fastapi.responses import FileResponse
import shutil

router = APIRouter()

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...), db=Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")

    file_location = f"images/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Images (filename, filepath) VALUES (?, ?)", (file.filename, file_location))
    conn.commit()
    conn.close()

    return {"info": f"File '{file.filename}' saved at '{file_location}'"}

@router.get("/image/{image_id}")
def get_image(image_id: int, db=Depends(get_db)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Images WHERE id = ?", (image_id,))
    image = cursor.fetchone()
    conn.close()

    if image:
        return FileResponse(image["filepath"])
    else:
        raise HTTPException(status_code=404, detail="Image not found")