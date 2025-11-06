from rest_framework import viewsets, permissions, generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Event, Ticket, Transfer, Cart, Profile
from .serializers import EventSerializer, TicketSerializer, TransferSerializer, RegisterSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
import random
from django.core.mail import send_mail
import uuid
from decimal import Decimal





class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

        
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.request.data.get("ticket")
        if not ticket_id:
            raise ValueError("Ticket ID is required")

        try:
            ticket = Ticket.objects.get(id=ticket_id, user=self.request.user)
        except Ticket.DoesNotExist:
            raise ValueError("Ticket not found or not owned by user")


        base_price = ticket.price
        resale_price = round(base_price * Decimal("1.2"))


        serializer.save(
            seller=self.request.user,
            ticket=ticket,
            price=resale_price,
        )



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        user = User.objects.get(username=request.data['username'])
        otp = random.randint(100000, 999999) 
        profile = Profile.objects.get(user=user)
        profile.verification_code = otp
        profile.save()
        print("✅ OTP stored:", profile.verification_code)
        
        subject = "Your TrueTix Verification Code"
        message = f"Hello!\n\nYour verification code is: {otp}\n\nThank you for using TrueTix."
        from_email = "truetix@outlook.com" 

        send_mail(
            subject,
            message,
            from_email,
            [user.email],
            fail_silently=False,
        )

        return response
        


class VerifyEmailView(APIView):
    
    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")

        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)

            if str(profile.verification_code) == str(code):
                user.is_active = True
                user.save()
                print("🧾 Submitted code:", code)
                print("📦 Stored code:", profile.verification_code)
                return Response({"message": "Account verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    try:
        event_id = request.data.get("event_id")
        seat_type = request.data.get("seat_type", "Front")
        event = Event.objects.get(id=event_id)
    
        if not event.tickets.filter(is_active=True, is_resell=False).exists():
            return Response({"error": "No available tickets for this event"}, status=400)

    

        seat_price_map = {
            "Front": event.price_front,
            "Behind Goal": event.price_behind_goal,
            "Home Side": event.price_side_home,
            "Away Side": event.price_side_away,
        }

        price = seat_price_map.get(seat_type, event.price_front)
        
        if Cart.objects.filter(user=request.user, event=event, seat_type=seat_type).exists():
            return Response({"message": "Event already in cart"}, status=400)

        Cart.objects.create(user=request.user, event=event, seat_type=seat_type, price=price)
        return Response({"message": "Event added to cart successfully!"}, status=201)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout_cart(request):
    try:  

        cart_items = Cart.objects.filter(user=request.user)
    
        if not cart_items.exists():
            return Response({"error": "Your cart is empty"}, status=400)


        for item in cart_items:
            print("Processing item:", item)
            Ticket.objects.create(
                user=request.user,
                event=item.event,
                seat_type=item.seat_type,
                price=item.price,
                qr_code=str(uuid.uuid4())    
            )

        cart_items.delete()

        return Response({"message": "Purchase confirmed! Tickets added to your account."}, status=200)
    
    except Exception as e:
        print("❌ Checkout error:", e)
        return Response({"error": str(e)}, status=500)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def resell_ticket(request):
    print("📦 Received data:", request.data)

    try:
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
        ticket_id = request.data.get("ticket")
        price = request.data.get("price")
        # new_price = round(ticket.event.price * Decimal("1.2"))
        new_price = Decimal(str(price))
        
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)

    if not ticket.is_active:
        return Response({"error": "Cannot resell inactive ticket"}, status=400)

    if ticket.is_resell:
        return Response({"error": "Ticket already listed for resale"}, status=400)

    Transfer.objects.create(
        ticket=ticket,
        seller=request.user,
        price=new_price,
        is_completed=False,


    )
    # ticket.is_active = False
    
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.is_resell = True
    ticket.status = "resell"
    ticket.save()



    return Response({"message": "Ticket listed for resale successfully!", "price": new_price}, status=201)


