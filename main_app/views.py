from rest_framework import viewsets, permissions, generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .models import Event, Ticket, Transfer, Profile
from .serializers import EventSerializer, TicketSerializer, TransferSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from django.core.mail import send_mail



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


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
            if user.profile.verification_code == code:
                user.is_active = True
                user.save()
                return Response({"message": "Account verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)