from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from database import get_db
from fastapi.responses import FileResponse
import shutil
import os
import datetime


router = APIRouter()

@router.post("/upload/")
async def upload_image(item_id: int, file: UploadFile = File(...), db=Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    
    # change filename to a unique name if needed

    if not os.path.exists("images"):
        os.makedirs("images")
    # use datatime
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_location = f"images/{timestamp}_{file.filename}"
    file_name = f"{timestamp}_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO Images (item_id, filename, filepath) VALUES (?, ?, ?)", 
        (item_id, file_name, file_location)
    )
    db.commit()

    return {"info": f"File '{file.filename}' saved at '{file_location}' for item_id {item_id}"}

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
    
@router.get("/items_with_images")
def get_items_with_images(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT DISTINCT
            i.id AS item_id,
            i.name,
            i.priceUSD,
            i.description,
            i.phone,
            i.city_id,
            c.name AS city_name,
            t.name AS type_name,
            (SELECT img.id FROM Images img WHERE img.item_id = i.id ORDER BY img.id ASC LIMIT 1) AS image_id,
            (SELECT COUNT(*) FROM UserLikedItems WHERE item_id = i.id) AS like_count
        FROM Item i
        LEFT JOIN Images img ON img.item_id = i.id
        LEFT JOIN City c ON i.city_id = c.id
        LEFT JOIN Type t ON i.type_id = t.id
        ORDER BY i.id DESC
    """)
    return [dict(row) for row in cursor.fetchall()]
