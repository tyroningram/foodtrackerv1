from pydantic import BaseModel, Field
class FoodBase(BaseModel):
    name: str = Field(..., examples=["Apple"])
    calories: int = Field(..., ge=0, examples=[95])
    carbs: int = Field(..., ge=0, examples=[25])
    protein: int = Field(..., ge=0, examples=[0])
    fat: int = Field(..., ge=0, examples=[0])


class FoodCreate(FoodBase):
    pass


class FoodUpdate(BaseModel):
    name: str | None = Field(None, examples=["Apple"])
    calories: int | None = Field(None, ge=0, examples=[95])
    carbs: int | None = Field(None, ge=0, examples=[25])
    protein: int | None = Field(None, ge=0, examples=[0])
    fat: int | None = Field(None, ge=0, examples=[0])


class FoodRead(FoodBase):
    id: int = Field(..., examples=[1000])
    
