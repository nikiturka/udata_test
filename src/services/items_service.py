from fastapi import HTTPException
from sqlalchemy import select
from src.db.models import Item


class ItemsService:
    @staticmethod
    def get_all_items(
        session
    ):
        query = select(Item)
        result = session.execute(query)
        items = result.scalars().all()

        return {"products": items}

    @staticmethod
    def get_item_by_name(
        product_name: str,
        session
    ):
        query = select(Item).where(Item.name == product_name)
        result = session.execute(query)
        item = result.scalar()

        if item is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return item
