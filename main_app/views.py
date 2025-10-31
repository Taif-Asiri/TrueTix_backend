from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Event, Ticket, Transfer
from .serializers import EventSerializer, TicketSerializer, TransferSerializer

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



