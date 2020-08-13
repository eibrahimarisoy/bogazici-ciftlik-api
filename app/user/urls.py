
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()
router.register('cities', views.CityViewSet)
router.register('districts', views.DistrictViewSet)
router.register('neighborhoods', views.NeighborhoodViewSet)


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', include(router.urls))
]
