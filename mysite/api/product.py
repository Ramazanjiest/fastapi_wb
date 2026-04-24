from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from db.database import SessionLocal
from db.models import Product,Category,SubCategory
from db.schema import ProductSchema
from typing import List

product_router = APIRouter(prefix='/product', tags=['Product'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/create', response_model=ProductSchema)
async def create_product(product_data: ProductSchema, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == product_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    subcategory = db.query(SubCategory).filter(SubCategory.id == product_data.sub_category_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@product_router.get('/list', response_model=List[ProductSchema])
async def list_product(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@product_router.get('/detail/{product_id}', response_model=ProductSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.put('/update/{product_id}', response_model=ProductSchema)
async def update_product(product_id: int, product_data: ProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_data.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@product_router.delete('/delete/{product_id}',response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"status": "Success deleted"}