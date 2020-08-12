from django.urls import include, path
from rest_framework.routers import DefaultRouter

from product import views

router = DefaultRouter()
router.register("categories", views.CategoryViewSet)
app_name = 'product'
urlpatterns = [
    path('', include(router.urls)),
    ]
