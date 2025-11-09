from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import ItemCreate, ItemResponse
from typing import Dict

router = APIRouter()

@router.post("/items/create", response_model=ItemResponse)
def create_item(item_data: ItemCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Item (user_id, name, priceUSD, type_id, description, phone, city_id) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (item_data.user_id, item_data.name, item_data.priceUSD, item_data.type_id, item_data.description, item_data.phone, item_data.city_id))
    db.commit()
    return {"id": cursor.lastrowid, **item_data.dict()}

@router.get("/items", response_model=list[ItemResponse])
def get_items(type_id: int = None, db=Depends(get_db)):
    cursor = db.cursor()
    if type_id:
        cursor.execute("SELECT * FROM Item WHERE type_id = ?", (type_id,))
    else:
        cursor.execute("SELECT * FROM Item")
    return [dict(row) for row in cursor.fetchall()]

@router.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE Item SET name = ?, priceUSD = ?, type_id = ? WHERE id = ?", 
                   (item_data.name, item_data.priceUSD, item_data.type_id, item_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db.commit()
    return {"id": item_id, **item_data.dict()}

@router.get("/items/{item_id}")
def get_item_detail(item_id: int, db=Depends(get_db)) -> Dict:
    """
    Return ONE item with:
      • All item fields
      • City name
      • Type name
      • Creator name (User.name)
      • First image URL (filepath + filename)
    """
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            i.id              AS item_id,
            i.name            AS title,
            i.priceUSD        AS price,
            i.description,
            i.phone,
            i.city_id,
            c.name            AS city_name,
            t.name            AS type_name,
            u.id              AS user_id,
            u.name            AS creator_name,
            -- First image (if any)
            img.id            AS image_id,
            img.filepath,
            img.filename,
            -- Like count from UserLikedItems table
            (SELECT COUNT(*) FROM UserLikedItems WHERE item_id = i.id) AS like_count
        FROM Item i
        LEFT JOIN User u      ON i.user_id = u.id
        LEFT JOIN City c      ON i.city_id = c.id
        LEFT JOIN Type t      ON i.type_id = t.id
        LEFT JOIN Images img  ON img.item_id = i.id
        WHERE i.id = ?
        ORDER BY img.id ASC
        LIMIT 1
    """, (item_id,))

    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    item = dict(row)

    # Build full image URL (adjust base URL if needed)
    if item.get("filepath") and item.get("filename"):
        # Example: /uploads/123/image.jpg
        item["image_url"] = f"/uploads/{item['filepath']}/{item['filename']}"
    else:
        item["image_url"] = None

    # Clean up internal fields
    for key in ["filename"]:
        item.pop(key, None)

    return item
    
@router.delete("/items/delete", response_model=dict)
def delete_item(item_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Item WHERE id = ?", (item_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db.commit()
    return {"message": "Item deleted"}

@router.get("/items/search", response_model=list[ItemResponse])
def search_items(query: str = "", type_name: str = "", min_price: int = 0, max_price: int = 1_000_000, page:int = 1, limit:int = 50, db=Depends(get_db)):
    
    offset = (page-1)*limit
    
    cursor = db.cursor()
    cursor.execute("""
        SELECT Item.* FROM Item
        JOIN Type ON Item.type_id = Type.id
        WHERE Item.name LIKE ? AND Type.name LIKE ? AND priceUSD BETWEEN ? AND ?
        LIMIT ? OFFSET ?
    """, (f"%{query}%", f"%{type_name}%", min_price, max_price, limit, offset))
    return [dict(row) for row in cursor.fetchall()]