```

uvicorn main:app --reload


POST /types - creates a type (name) 
# for your site: house, car, job

GET  /types - gives you all types

POST /items/create - creates an item (name, priceUSD, type_id)
GET  /items - all items
PUT  /items/<item_id> - update an item
DELETE /items/<item_id> - deletes an item

GET /items/search?
                query=?
                type_name=?
                min_price=?
                max_price=? - search by query, type, price

POST /users/register - creates a user (name, password)

POST /users/login 
POST /users/logout
# those two can vary and depend on your authentification
# so for now they measure your rizz

POST /users/<user_id>/liked/<item_id> - one way of liking
POST /users/like - another way. just send JSON with ids

GET /users/<user_id/liked-items> - shows all of the liked items

```


