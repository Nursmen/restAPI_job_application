from pydantic import BaseModel

class TypeBase(BaseModel):
    name: str

class TypeCreate(TypeBase):
    pass

class TypeResponse(TypeBase):
    id: int

class ItemBase(BaseModel):
    name: str
    priceUSD: int
    type_id: int
    user_id: int
    city_id: int
    description: str
    phone: str

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

class User(BaseModel):
    name: str
    password: str

class LikeRequest(BaseModel):
    user_id: int
    item_id: int


class CommentBase(BaseModel):
    user_id: int
    item_id: int
    text: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int