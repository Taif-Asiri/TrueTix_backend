from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]