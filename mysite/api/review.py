from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from db.database import SessionLocal
from db.models import Review, Product
from db.schema import ReviewSchema
from typing import List

review_router = APIRouter(prefix='/review', tags=['Review'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/create', response_model=ReviewSchema)
async def create_review(review_data: ReviewSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == review_data.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    review = Review(**review_data.dict())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@review_router.get('/list', response_model=List[ReviewSchema])
async def list_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return reviews


@review_router.get('/detail/{review_id}', response_model=ReviewSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Review not found')
    return review

@review_router.put('/update/{review_id}', response_model=ReviewSchema)
async def update_review(review_id: int, review_data: ReviewSchema, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Review not found')
    for key, value in review_data.dict().items():
        setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return review

@review_router.delete('/delete/{review_id}')
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Review not found')
    db.delete(review)
    db.commit()
    return {"status": "Success deleted"}