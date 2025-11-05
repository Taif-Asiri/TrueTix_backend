from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, TicketViewSet, TransferViewSet, RegisterView, VerifyEmailView, UserProfileView, add_to_cart, get_cart, checkout_cart
from . import views


router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'transfers', TransferViewSet)
# router.register(r'cart', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyEmailView.as_view(), name='verify'),
    path('profile/', UserProfileView.as_view(), name='UserProfile'),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.get_cart, name="get_cart"),
    path("cart/checkout/", views.checkout_cart, name="checkout_cart"),
    path("resell/", views.resell_ticket, name="resell_ticket"),



]
