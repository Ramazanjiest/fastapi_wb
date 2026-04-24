from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from db.database import SessionLocal
from db.models import Category
from db.schema import CategorySchema
from typing import List

category_router = APIRouter(prefix='/category', tags=['Category'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@category_router.post('/create', response_model=CategorySchema)
async def create_category(category_data: CategorySchema, db: Session = Depends(get_db)):
    category_db = Category(**category_data.dict())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

@category_router.get('/list', response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    category_db = db.query(Category).all()
    return category_db

@category_router.get('/detail/{category_id}', response_model=CategorySchema)
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    return category_db

@category_router.put('/update/{category_id}', response_model=CategorySchema)
async def update_category(category_id: int, category_data: CategorySchema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    for key, value in category_data.dict().items():
        setattr(category_db, key, value)
    db.commit()
    db.refresh(category_db)
    return category_db

@category_router.delete('/delete/{category_id}', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db =  db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    db.delete(category_db)
    db.commit()
    return {'status': 'Success deleted'}


