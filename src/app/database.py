import sqlite3
from .schemas.food import FoodCreate, FoodUpdate
from typing import Any


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("foodtracker.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self, ):
        self.cursor.execute(
            """
               CREATE TABLE IF NOT EXISTS food_entries
               (id INTEGER PRIMARY KEY, name TEXT, calories FLOAT, carbs INTEGER, protein INTEGER, fat INTEGER)
               """
        )

    def insert_food_entry(self, entry: FoodCreate) -> int:
        self.cursor.execute("SELECT MAX(id) FROM food_entries")
        max_id = self.cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        self.cursor.execute(
            """
                            INSERT INTO food_entries (id, name, calories, carbs, protein, fat)
                            VALUES (:id, :name, :calories, :carbs, :protein, :fat)
                            """,
            {"id": new_id, **entry.model_dump()},
        )
        self.connection.commit()
        return new_id

    def get_food_entry(self, food_id: int) -> dict[str, Any] | None:
        self.cursor.execute(
            """
               SELECT * FROM food_entries 
               WHERE id = ?
               """,
            (food_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "calories": row[2],
                "carbs": row[3],
                "protein": row[4],
                "fat": row[5],
            }
        else:
            return None

    
    def get_all_food_entries(self) -> list[dict[str, Any]]:
        self.cursor.execute(
            """
               SELECT * FROM food_entries
               """
        )
        rows = self.cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "calories": row[2],
                "carbs": row[3],
                "protein": row[4],
                "fat": row[5],
            }
            for row in rows
        ]

    def update_food_entry(self, food_id: int, entry: FoodUpdate) -> int:
        self.cursor.execute(
            """
               UPDATE food_entries 
               SET name = :name, calories = :calories, carbs = :carbs, protein = :protein, fat = :fat
               WHERE id = :id
               """,
            {"id": food_id, **entry.model_dump()},
        )
        self.connection.commit()
        return self.get_food_entry(food_id)

    def delete_food_entry(self, food_id: int) -> None:
        self.cursor.execute(
            """
               DELETE FROM food_entries 
               WHERE id = ?
               """,
            (food_id,),
        )
        self.connection.commit()

    def close(self):
        self.connection.close()
