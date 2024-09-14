from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_session
from src.services.items_service import ItemsService

items_router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@items_router.get("/all_products/")
async def get_all_products(session: Session = Depends(get_session)):
    items = ItemsService.get_all_items(session)

    return {"products": items}


@items_router.get("/products/{product_name}")
async def get_all_products(
    product_name: str,
    session: Session = Depends(get_session)
):
    item = ItemsService.get_item_by_name(product_name, session)

    return {"product": item}


@items_router.get("/products/{product_name}/{product_field}")
async def get_product_field(
    product_name: str,
    product_field: str,
    session: Session = Depends(get_session)
):
    item = ItemsService.get_item_by_name(product_name, session)

    if not hasattr(item, product_field):
        raise HTTPException(status_code=400, detail="Invalid product field")

    return {product_field: getattr(item, product_field)}
