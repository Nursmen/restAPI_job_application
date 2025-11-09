from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import CommentCreate, CommentResponse

router = APIRouter()

@router.post("/comments", response_model=CommentResponse)
def create_comment(comment_data: CommentCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO Comment (user_id, item_id, text) VALUES (?, ?, ?)",
        (comment_data.user_id, comment_data.item_id, comment_data.text),
    )
    db.commit()
    return {
        "id": cursor.lastrowid,
        "user_id": comment_data.user_id,
        "item_id": comment_data.item_id,
        "text": comment_data.text,
    }

@router.get("/comments/{item_id}", response_model=list[CommentResponse])
def get_comments(item_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Comment WHERE item_id = ?", (item_id,))
    comments = cursor.fetchall()
    return [dict(row) for row in comments]
