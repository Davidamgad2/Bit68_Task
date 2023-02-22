from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('Register',views.UserProfileViewSet,basename='Register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/',views.UserLoginApiView.as_view(),name='login'),
    path('product/',views.order_products,name='main_product_page'),
    path('product/search/',views.product_search,name='search'),
    path('cart/',views.get_cart,name='get cart'),
    path('cart/add',views.add_to_cart,name='add to cart'),
]
