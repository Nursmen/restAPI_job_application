from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import User, LikeRequest

router = APIRouter()

@router.post("/users/register")
def register(type_data: User, db=Depends(get_db)):
    cursor = db.cursor()

    if len(type_data.password) < 6:
        return {'error': 400, 'message': "Password is just too little"}

    cursor.execute("INSERT INTO User (name, password) VALUES (?, ?)",
                    (type_data.name, type_data.password))

    db.commit()
    return {"id": cursor.lastrowid, 'name':type_data.name}

@router.post("/users/login")
def login(type_data: User, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM User WHERE name = ? AND password = ?",
                    (type_data.name, type_data.password))
    if cursor.fetchall() == []:
        raise HTTPException(status_code=400, detail="U have no aura. Your rizz is skibidi 👎")

    return {'message': "Hello 👋"}

@router.post("/users/logout")
def logout(type_data: User, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM User WHERE name = ? AND password = ?",
                    (type_data.name, type_data.password))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=400, detail="U have no aura. Your rizz is skibidi 👎")

    return {'message': "Done 👋"}

@router.get("/users/{user_id}/liked-items")
def get_liked_items(user_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT Item.* FROM Item
        JOIN UserLikedItems ON Item.id = UserLikedItems.item_id
        WHERE UserLikedItems.user_id = ?
    """, (user_id,))
    return [dict(row) for row in cursor.fetchall()]

@router.post("/users/{user_id}/like/{item_id}")
def like_item(user_id: int, item_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO UserLikedItems (user_id, item_id) VALUES (?, ?)", (user_id, item_id))
    db.commit()
    return {"message": "Item liked"}

@router.post("/users/like")
def like_item(data: LikeRequest, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO UserLikedItems (user_id, item_id) VALUES (?, ?)", 
                   (data.user_id, data.item_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=400, detail="Item already liked or invalid IDs")
    return {"message": "Item liked"}