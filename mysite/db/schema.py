from pydantic import BaseModel
from typing import Optional


class RegisterSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    phone_number: str
    age: Optional[str]
    profile_image: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

class UserProfileSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    phone_number: str
    age: int
    profile_image: str

class UserProfileReponseSchema(BaseModel):
    phone_number: str
    age: int
    profile_image: str

class CategorySchema(BaseModel):
    category_name: str
    category_image: str

class SubCategorySchema(BaseModel):
    category_id: int
    sub_category_name: str

class ProductSchema(BaseModel):
    category_id: int
    sub_category_id: int
    product_name: str
    description: str
    price: int
    product_image: str

class ImageProductSchema(BaseModel):
    product_id: int
    image: str

class ReviewSchema(BaseModel):
    user_id: int
    product_id: int
    images: Optional[str]
    video: Optional[str]
    comments: Optional[str]
    stars: Optional[str]

class CartSchema(BaseModel):
    user_id: int
    product_id: int
    images: Optional[str]

class CartItemSchema(BaseModel):
    cart_id: int
    product_id: int

class FavoriteSchema(BaseModel):
    user_id: int
    product_id: int
    like: bool


