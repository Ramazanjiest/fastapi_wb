from .view import UserProfileView,CategoryView,SubCategoryView,ProductView,CartView,CartItemView,ReviewView,FavoriteView,ImageProductView
from sqladmin import Admin
from fastapi import FastAPI
from db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine=engine)
    admin.add_view(UserProfileView)
    admin.add_view(CategoryView)
    admin.add_view(SubCategoryView)
    admin.add_view(ProductView)
    admin.add_view(CartView)
    admin.add_view(CartItemView)
    admin.add_view(ReviewView)
    admin.add_view(FavoriteView)
    admin.add_view(ImageProductView)
