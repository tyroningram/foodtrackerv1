from fastapi import FastAPI, HTTPException, status
from typing import Any

from .schemas.food import FoodCreate, FoodUpdate

app = FastAPI()

test_data = {
    1000: {"name": "Apple", "calories": 95, "carbs": 25, "protein": 0.5, "fat": 0.3},
    1001: {"name": "Banana", "calories": 105, "carbs": 27, "protein": 1.3, "fat": 0.4},
    1002: {
        "name": "Chicken Breast",
        "calories": 165,
        "carbs": 0,
        "protein": 31,
        "fat": 3.6,
    },
}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Food Tracker API!"}


@app.get("/foods")
async def read_database():
    return test_data


@app.get("/food")
async def read_food(food_id: int | None = None) -> dict[str, Any]:
    food_item = test_data.get(food_id)
    if food_item:
        return food_item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")


@app.post("/food")
async def add_food(body: FoodCreate) -> dict[str, Any]:

    food_id = max(test_data.keys()) + 1
    name = body.name
    calories = body.calories
    carbs = body.carbs
    protein = body.protein
    fat = body.fat

    if food_id in test_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Food item with this ID already exists")

    test_data[food_id] = {
        "name": name,
        "calories": calories,
        "carbs": carbs,
        "protein": protein,
        "fat": fat,
    }
    return {"message": "Food item added successfully", "food_item": test_data[food_id]}


@app.delete("/food")
async def delete_food(food_id: int) -> dict[str, Any]:
    if food_id in test_data:
        deleted_item = test_data.pop(food_id)
        return {
            "message": "Food item deleted successfully",
            "deleted_item": deleted_item,
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")


@app.put("/food")
async def update_food(food_id: int, body: FoodUpdate) -> dict[str, Any]:
    if food_id in test_data:
        name = body.name
        calories = body.calories
        carbs = body.carbs
        protein = body.protein
        fat = body.fat

        test_data[food_id] = {
            "name": name,
            "calories": calories,
            "carbs": carbs,
            "protein": protein,
            "fat": fat,
        }
        return {
            "message": "Food item updated successfully",
            "food_item": test_data[food_id],
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
    

@app.patch("/food")
async def patch_food(food_id: int, body: FoodUpdate) -> dict[str, Any]:
    if food_id in test_data:
        food_item = test_data[food_id]

        name = body.name if body.name is not None else food_item["name"]
        calories = body.calories if body.calories is not None else food_item["calories"]
        carbs = body.carbs if body.carbs is not None else food_item["carbs"]
        protein = body.protein if body.protein is not None else food_item["protein"]
        fat = body.fat if body.fat is not None else food_item["fat"]

        test_data[food_id] = {
            "name": name,
            "calories": calories,
            "carbs": carbs,
            "protein": protein,
            "fat": fat,
        }
        return {
            "message": "Food item patched successfully",
            "food_item": test_data[food_id],
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")

