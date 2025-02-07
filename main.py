from fastapi import FastAPI
from routers import items, types, users

app = FastAPI()

app.include_router(types.router)
app.include_router(items.router)
app.include_router(users.router)
