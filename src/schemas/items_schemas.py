from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str
    calories: int
    fats: int
    carbs: int
    proteins: int
    unsaturated_fats: float
    sugar: float
    salt: float
    portion: float
