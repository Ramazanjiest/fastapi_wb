from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from db.database import SessionLocal
from db.models import Cart
from db.schema import CartSchema
from typing import List

cart_router = APIRouter(prefix='/cart', tags=['Cart'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cart_router.post('/create', response_model=CartSchema)
async def create_cart(cart_data: CartSchema, db: Session = Depends(get_db)):
    cart = Cart(**cart_data.dict())
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

@cart_router.get('/list', response_model=List[CartSchema])
async def list_carts(db: Session = Depends(get_db)):
    carts = db.query(Cart).all()
    return carts

@cart_router.get('/detail/{cart_id}', response_model=CartSchema)
async def detail_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cart not found')
    return cart

@cart_router.delete('/delete/{cart_id}')
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cart not found')
    db.delete(cart)
    db.commit()
    return {"status": "Success deleted"}