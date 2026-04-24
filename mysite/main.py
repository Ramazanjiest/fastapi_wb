from fastapi import FastAPI
from api import user,category,subcategory,auth,image,review,cart
from admin.settup import setup_admin


wildberies_app = FastAPI()
wildberies_app.include_router(user.user_router)
wildberies_app.include_router(category.category_router)
wildberies_app.include_router(subcategory.subcategory_router)
wildberies_app.include_router(auth.auth_router)
wildberies_app.include_router(image.image_product_router)
wildberies_app.include_router(review.review_router)
wildberies_app.include_router(cart.cart_router)

setup_admin(wildberies_app)