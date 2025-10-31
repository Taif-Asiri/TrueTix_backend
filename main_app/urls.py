from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, TicketViewSet, TransferViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'transfers', TransferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
