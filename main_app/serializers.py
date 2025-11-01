from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Ticket, Transfer
import random
from django.core.mail import send_mail



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

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email', 'password', ]
        extra_kwargs = {'password': {'write_only': True}}
        
        def validate_email(self, value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email is already in use.")
            return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )

        
        
        return user