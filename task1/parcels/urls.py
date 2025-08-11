from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LetterViewSet, ParcelViewSet

router = DefaultRouter()
router.register(r'letters', LetterViewSet, basename='letter')
router.register(r'parcels', ParcelViewSet, basename='parcel')

urlpatterns = [
    path('', include(router.urls)),
]