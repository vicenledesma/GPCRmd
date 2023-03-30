from django.urls import include, re_path
from rest_framework import routers

from . import views

# Routers
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^api_auth/', include('rest_framework.urls')),

]