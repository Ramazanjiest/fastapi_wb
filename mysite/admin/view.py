from sqladmin import ModelView
from db.models import UserProfile,Category,SubCategory,Product,Cart,CartItem,Review,Favorite,ImageProduct

class UserProfileView(ModelView,model=UserProfile):
    column_list = [UserProfile.id,UserProfile.username]

class CategoryView(ModelView,model=Category):
    column_list = [Category.id]

class SubCategoryView(ModelView,model=SubCategory):
    column_list = [SubCategory.id]

class ProductView(ModelView,model=Product):
    column_list = [Product.id]

class ReviewView(ModelView,model=Review):
    column_list = [Review.id]

class FavoriteView(ModelView,model=Favorite):
    column_list = [Favorite.id]

class ImageProductView(ModelView,model=ImageProduct):
    column_list = [ImageProduct.id]

class CartView(ModelView,model=Cart):
    column_list = [Cart.id]

class CartItemView(ModelView,model=CartItem):
    column_list = [CartItem.id]


