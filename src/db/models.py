from typing import Annotated
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str]
    calories: Mapped[str]
    fats: Mapped[str]
    carbs: Mapped[str]
    proteins: Mapped[str]
    unsaturated_fats: Mapped[str]
    sugar: Mapped[str]
    salt: Mapped[str]
    portion: Mapped[str]

    def __repr__(self):
        return (f"<Item(id={self.id}, name='{self.name}', description='{self.description}', "
                f"calories={self.calories}, fats={self.fats}, carbs={self.carbs}, "
                f"proteins={self.proteins}, unsaturated_fats={self.unsaturated_fats}, "
                f"sugar={self.sugar}, salt={self.salt}, portion={self.portion})>")

    def __str__(self):
        return (f"Item - ID: {self.id}, Name: {self.name}, Description: {self.description}, "
                f"Calories: {self.calories}, Fats: {self.fats}, Carbs: {self.carbs}, "
                f"Proteins: {self.proteins}, Unsaturated Fats: {self.unsaturated_fats}, "
                f"Sugar: {self.sugar}, Salt: {self.salt}, Portion: {self.portion}")
