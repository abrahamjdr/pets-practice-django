"""
URL configuration for the authentication system
"""
from django.urls import path, include
from rest_framework import routers
from . import views

"""
Router configuration
"""
router = routers.DefaultRouter()

"""
Registers the UserViewSet with the router, using the basename 'pets'.
This will create the following URLs:
    - /pets/ (GET, POST)
    - /pets/{pk}/ (GET, PUT, PATCH, DELETE)
"""
router.register(r'', views.PetsViewSet, basename='pets')


"""
URL patterns
    Includes the URLs generated by the router.
    This will include the URLs for the UserViewSet.
"""
urlpatterns = [
    path('', include(router.urls)),
]
