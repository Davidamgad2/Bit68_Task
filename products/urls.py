from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('Register',views.UserProfileViewSet,basename='Register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/',views.UserLoginApiView.as_view()),
    path('product/',views.products_view)
]
