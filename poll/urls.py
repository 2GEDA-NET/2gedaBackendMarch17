from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'votes', views.VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
