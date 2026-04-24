from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from db.database import SessionLocal
from db.models import SubCategory,Category
from db.schema import SubCategorySchema
from typing import List

subcategory_router = APIRouter(prefix='/subcategory', tags=['SubCategory'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@subcategory_router.post('/create', response_model=SubCategorySchema)
async def create_subcategory(subcategory_data: SubCategorySchema, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == subcategory_data.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    subcategory_db = SubCategory(**subcategory_data.dict())
    db.add(subcategory_db)
    db.commit()
    db.refresh(subcategory_db)
    return subcategory_db

@subcategory_router.get('/list', response_model=List[SubCategorySchema])
async def list_subcategory(db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).all()
    return subcategory_db

@subcategory_router.get('/detail/{subcategory_id}', response_model=SubCategorySchema)
async def detail_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    return subcategory

@subcategory_router.put('/update/{subcategory_id}', response_model=SubCategorySchema)
async def update_subcategory(subcategory_id: int, subcategory_data: SubCategorySchema, db: Session = Depends(get_db)):
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    for key, value in subcategory_data.dict().items():
        setattr(subcategory, key, value)
    db.commit()
    db.refresh(subcategory)
    return subcategory

@subcategory_router.delete('/delete/{subcategory_id}',response_model=dict)
async def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    db.delete(subcategory)
    db.commit()
    return {"status": "Success deleted"}
