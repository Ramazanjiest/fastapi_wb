from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from db.database import SessionLocal
from db.models import ImageProduct, Product
from db.schema import ImageProductSchema
from typing import List

image_product_router = APIRouter(prefix='/image-product', tags=['ImageProduct'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@image_product_router.post('/create', response_model=ImageProductSchema)
async def create_image(image_data: ImageProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == image_data.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    image = ImageProduct(**image_data.dict())
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@image_product_router.get('/list', response_model=List[ImageProductSchema])
async def list_images(db: Session = Depends(get_db)):
    images = db.query(ImageProduct).all()
    return images


@image_product_router.get('/detail/{image_id}', response_model=ImageProductSchema)
async def detail_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ImageProduct).filter(ImageProduct.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image

@image_product_router.put('/update/{image_id}', response_model=ImageProductSchema)
async def update_image(image_id: int, image_data: ImageProductSchema, db: Session = Depends(get_db)):
    image = db.query(ImageProduct).filter(ImageProduct.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    for key, value in image_data.dict().items():
        setattr(image, key, value)
    db.commit()
    db.refresh(image)
    return image

@image_product_router.delete('/delete/{image_id}')
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ImageProduct).filter(ImageProduct.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    db.delete(image)
    db.commit()

    return {"status": "Success deleted"}