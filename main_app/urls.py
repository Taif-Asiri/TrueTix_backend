from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, TicketViewSet, TransferViewSet, RegisterView, VerifyEmailView, CartViewSet, add_to_cart, get_cart, checkout_cart
from . import views


router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'transfers', TransferViewSet)
router.register(r'cart', CartViewSet)


urlpatterns = [
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/checkout/", views.checkout_cart, name="checkout_cart"),
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyEmailView.as_view(), name='verify'),
    path("resell/", views.resell_ticket, name="resell_ticket"),



]
