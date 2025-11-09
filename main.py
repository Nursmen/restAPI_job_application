from fastapi import FastAPI
from routers import items, types, users, images, cities, comments
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://127.0.0.1:5500"] for example
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("images", exist_ok=True)
app.mount("/images", StaticFiles(directory="images"), name="images")

app.include_router(types.router)
app.include_router(items.router)
app.include_router(users.router)
app.include_router(images.router)
app.include_router(cities.router)
app.include_router(comments.router)