from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import ItemCreate, ItemResponse

router = APIRouter()

@router.post("/items/create", response_model=ItemResponse)
def create_item(item_data: ItemCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Item (name, priceUSD, type_id) VALUES (?, ?, ?)", 
                   (item_data.name, item_data.priceUSD, item_data.type_id))
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
    
@router.delete("/items/delete", response_model=dict)
def delete_item(item_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Item WHERE id = ?", (item_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    db.commit()
    return {"message": "Item deleted"}

@router.get("/items/search", response_model=list[ItemResponse])
def search_items(query: str = "", type_name: str = "", min_price: int = 0, max_price: int = 1_000_000, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT Item.* FROM Item
        JOIN Type ON Item.type_id = Type.id
        WHERE Item.name LIKE ? AND Type.name LIKE ? AND priceUSD BETWEEN ? AND ?
    """, (f"%{query}%", f"%{type_name}%", min_price, max_price))
    return [dict(row) for row in cursor.fetchall()]