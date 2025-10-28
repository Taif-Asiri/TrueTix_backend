from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Ticket, Transfer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  
    event = EventSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Transfer
        fields = '__all__'
