# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a classified ads/marketplace REST API built with FastAPI and SQLite, featuring a frontend template for displaying items (jobs, houses, cars, etc.). Users can create items, like items, comment, and upload images.

## Running the Application

**Start the API server:**
```bash
uvicorn main:app --reload
```

The API runs on `http://127.0.0.1:8000` by default.

**Frontend:**
The HTML frontend is in the `anime-main/` directory. Open `index.html` in a browser or use a local server (e.g., Live Server extension). The frontend expects the API to be running on `http://127.0.0.1:8000`.

## Architecture

### Backend Structure

**Entry Point:** `main.py`
- FastAPI application with CORS middleware configured to allow all origins
- Mounts static file serving for `/images` directory
- Includes all router modules

**Database:** SQLite (`sales.db`)
- Managed in `database.py` with `init_db()` creating tables on startup
- Uses `sqlite3.Row` for row_factory to return dict-like objects
- Main tables:
  - `User` - user accounts (name, password - no hashing currently)
  - `Item` - marketplace items with foreign keys to User, Type, and City
  - `Type` - item categories (e.g., house, car, job)
  - `City` - location data
  - `Images` - file metadata with foreign key to Item
  - `UserLikedItems` - many-to-many relationship for likes
  - `Comment` - user comments on items

**Routers:** Each domain has its own router in `routers/`:
- `items.py` - CRUD for items, search with pagination
- `users.py` - registration, login, logout, user-item relationships
- `images.py` - image upload and retrieval, `/items_with_images` endpoint
- `comments.py` - comment CRUD
- `types.py` - item type management
- `cities.py` - city management

**Models:** `models.py`
- Pydantic models for request/response validation
- Follows pattern: `Base`, `Create`, and `Response` models for each entity

### Frontend Structure

**Location:** `anime-main/` directory
- Based on an anime/video template (Colorlib)
- Main pages:
  - `index.html` - displays all items from `/items_with_images`
  - `anime-details.html` - single item view with comments and like functionality
  - `index copy.html` - user profile page showing liked and uploaded items (displays first 3 with "View All" toggle)
  - `login.html`, `signup.html` - authentication forms
  - `anime-watching.html` - create new item form

**Frontend-Backend Integration:**
- API calls hardcoded to `http://127.0.0.1:8000`
- Uses `localStorage` to store logged-in user data (key: `"user"`, value: JSON with `{id, name}`)
- Images fetched via `/image/{image_id}` endpoint
- Like functionality: POST to `/users/{user_id}/like/{item_id}`

### Key Architectural Patterns

**Like Count Display:**
When displaying like counts, backend endpoints use a subquery:
```sql
(SELECT COUNT(*) FROM UserLikedItems WHERE item_id = i.id) AS like_count
```
This pattern is used in:
- `/items/{item_id}` endpoint in `routers/items.py`
- `/items_with_images` endpoint in `routers/images.py`

**Image Handling:**
- Upload: POST `/upload/` with multipart form data (requires `item_id` and `file`)
- Files stored in `images/` directory with timestamp prefix
- Retrieval: GET `/image/{image_id}` returns `FileResponse` with filepath from database
- Frontend displays images via `background-image` CSS or direct `<img>` tags

**Item Display Pattern:**
Frontend uses a consistent pattern for rendering items with image, price, type, city, comment count, and like count. The `renderItem()` function is reused across pages.

## Database Schema Notes

- **UserLikedItems** uses composite primary key `(user_id, item_id)` with `INSERT OR IGNORE` for idempotent likes
- **Images** table stores both `filename` and `filepath` (filepath includes `images/` prefix)
- **Item** has no direct relationship to Images table in schema, but joined via `item_id` foreign key

## API Authentication

Currently implements basic authentication without JWT or sessions:
- Login returns user `{id, name}` which frontend stores in localStorage
- No actual session management or token validation
- Logout endpoint exists but doesn't invalidate anything server-side

## Common Endpoints

**Items:**
- GET `/items_with_images` - all items with first image and metadata (includes like_count)
- GET `/items/{item_id}` - single item detail with all metadata (includes like_count)
- POST `/items/create` - create item (requires user_id, name, priceUSD, type_id, description, phone, city_id)
- GET `/items/search?query=&type_name=&min_price=&max_price=&page=&limit=` - search with pagination

**Users:**
- POST `/users/register` - create user (name, password min 6 chars, no spaces)
- POST `/users/login` - authenticate (returns id and name)
- GET `/users/{user_id}/liked-items` - returns items with image_id
- GET `/users/{user_id}/uploaded-items` - returns items with image_id
- POST `/users/{user_id}/like/{item_id}` - like an item (idempotent)

**Comments:**
- GET `/comments/{item_id}` - all comments for item
- POST `/comments` - create comment (user_id, item_id, text)

## Known Patterns and Conventions

1. **Frontend uses two different item fetching strategies:**
   - `anime-details.html` first loads from `/items_with_images`, then also calls `/items/{item_id}` for detailed data
   - This is somewhat redundant but maintains compatibility with existing code

2. **Background image application:**
   Frontend uses jQuery `.set-bg` pattern and manual `data-setbg` attribute application via JavaScript

3. **Like count real-time updates:**
   When user clicks like, frontend refetches item data to update like_count display

4. **User profile page (index copy.html):**
   Implements "View All" toggle that shows 3 items initially, expands to show all on button click

## File Upload Workflow

1. Frontend creates FormData with `item_id` and `file`
2. POST to `/upload/` endpoint
3. Backend saves to `images/{timestamp}_{filename}`
4. Database stores both filename and filepath
5. Frontend fetches via `/image/{image_id}` which returns FileResponse

## CLI Tool

`cli.py` - Command-line interface for database operations (appears to be for debugging/admin tasks)