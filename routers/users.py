from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import User, LikeRequest
from typing import List, Dict

router = APIRouter()

@router.post("/users/register")
def register(type_data: User, db=Depends(get_db)):
    cursor = db.cursor()

    if len(type_data.password) < 6:
        return {'error': 400, 'message': "Password is just too little"}

    if type_data.name == "" or type_data.password == "":
        return {'error': 400, 'message': "Fields cant be empty"}
    
    if " " in type_data.name or " " in type_data.password:
        return {'error': 400, 'message': "Fields cant contain spaces"}
    
    # check if user already exists
    cursor.execute("SELECT * FROM User WHERE name = ?", (type_data.name,))
    if cursor.fetchall() != []:
        return {'error': 400, 'message': "User with this name already exists"}

    cursor.execute("INSERT INTO User (name, password) VALUES (?, ?)",
                    (type_data.name, type_data.password))

    db.commit()
    return {"id": cursor.lastrowid, 'name':type_data.name}

@router.post("/users/login")
def login(type_data: User, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, name FROM User WHERE name = ? AND password = ?",
        (type_data.name, type_data.password)
    )
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль 👎")

    return {"message": "Hello 👋", "id": user[0], "name": user[1]}


@router.post("/users/logout")
def logout(type_data: User, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM User WHERE name = ? AND password = ?",
                    (type_data.name, type_data.password))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль 👎")

    return {'message': "Done 👋"}

@router.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM User WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

@router.get("/users/{user_id}/uploaded-items")
def get_uploaded_items(user_id: int, db=Depends(get_db)) -> List[Dict]:
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            i.*,
            img.id AS image_id
        FROM Item i
        LEFT JOIN Images img ON img.item_id = i.id
        WHERE i.user_id = ?
        ORDER BY img.id ASC
    """, (user_id,))

    items = cursor.fetchall()
    result = []
    seen = set()

    for row in items:
        item_id = row["id"]
        if item_id in seen:
            continue
        seen.add(item_id)

        item = dict(row)
        if "image_id" in item and item["image_id"] is not None:
            pass  
        else:
            item["image_id"] = None

        result.append(item)

    return result


@router.get("/users/{user_id}/liked-items")
def get_liked_items(user_id: int, db=Depends(get_db)) -> List[Dict]:
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            i.*,
            img.id AS image_id
        FROM Item i
        JOIN UserLikedItems uli ON i.id = uli.item_id
        LEFT JOIN Images img ON img.item_id = i.id
        WHERE uli.user_id = ?
        ORDER BY img.id ASC
    """, (user_id,))

    items = cursor.fetchall()
    result = []
    seen = set()

    for row in items:
        item_id = row["id"]
        if item_id in seen:
            continue
        seen.add(item_id)

        item = dict(row)
        item["image_id"] = item.get("image_id")  # may be None

        result.append(item)

    return result

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