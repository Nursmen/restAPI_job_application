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