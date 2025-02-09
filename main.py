from fastapi import FastAPI
from routers import items, types, users, images, cities
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

os.makedirs("images", exist_ok=True)
app.mount("/images", StaticFiles(directory="images"), name="images")

app.include_router(types.router)
app.include_router(items.router)
app.include_router(users.router)
app.include_router(images.router)
app.include_router(cities.router)