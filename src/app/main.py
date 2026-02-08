from fastapi import FastAPI
from typing import Any

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


@app.get("/database")
async def read_database():
    return test_data


@app.get("/food")
async def read_food(food_id: int | None = None) -> dict[str, Any]:
    food_item = test_data.get(food_id)
    if food_item:
        return food_item
    else:
        return {"error": "Food item not found"}


@app.post("/food")
async def add_food(body: dict[str, Any]) -> dict[str, Any]:

    food_id = max(test_data.keys()) + 1
    name = body.get("name")
    calories = body.get("calories")
    carbs = body.get("carbs")
    protein = body.get("protein")
    fat = body.get("fat")

    if food_id in test_data:
        return {"error": "Food item with this ID already exists"}

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
        return {"error": "Food item not found"}


@app.put("/food")
async def update_food(food_id: int, body: dict[str, Any]) -> dict[str, Any]:
    if food_id in test_data:
        name = body.get("name")
        calories = body.get("calories")
        carbs = body.get("carbs")
        protein = body.get("protein")
        fat = body.get("fat")

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
        return {"error": "Food item not found"}

