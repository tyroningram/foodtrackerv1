from fastapi import FastAPI, HTTPException, status
from typing import Any

from .schemas.food import FoodCreate, FoodUpdate
from .database import Database

app = FastAPI()

db = Database()

# test_data = {
#     1000: {"name": "Apple", "calories": 95, "carbs": 25, "protein": 0.5, "fat": 0.3},
#     1001: {"name": "Banana", "calories": 105, "carbs": 27, "protein": 1.3, "fat": 0.4},
#     1002: {
#         "name": "Chicken Breast",
#         "calories": 165,
#         "carbs": 0,
#         "protein": 31,
#         "fat": 3.6,
#     },
# }


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Food Tracker API!"}


@app.get("/foods")
async def read_database():
    db_entries = db.get_all_food_entries()
    return db_entries


@app.get("/food")
async def read_food(food_id: int | None = None) -> dict[str, Any]:
    food_entry = db.get_food_entry(food_id)
    if food_entry:
        return food_entry
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found"
        )


@app.post("/food")
async def add_food(body: FoodCreate) -> dict[str, Any]:
    food_id = db.insert_food_entry(body)
    return {"message": "Food item added successfully", "food_item": db.get_food_entry(food_id)}


@app.delete("/food")
async def delete_food(food_id: int) -> dict[str, Any]:
    food_entry = db.get_food_entry(food_id)
    if food_entry:
        db.delete_food_entry(food_id)
        return {"message": "Food item deleted successfully", "deleted_item": food_entry}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found"
        )


@app.put("/food")
async def update_food(food_id: int, body: FoodUpdate) -> dict[str, Any]:

    updated_food = db.update_food_entry(food_id, body)
    return {
            "message": "Food item updated successfully",
            "food_item": updated_food,
        }


@app.patch("/food")
async def patch_food(food_id: int, body: FoodUpdate) -> dict[str, Any]:
    updated_food = db.update_food_entry(food_id, body)
    return {
            "message": "Food item updated successfully",
            "food_item": updated_food,
        }