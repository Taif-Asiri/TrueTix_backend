from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Ticket, Transfer, Cart
import random
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', "is_active"]
        read_only_fields = ['username']
        
    
        
class CartSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.name", read_only=True)
    event_date = serializers.DateTimeField(source="event.date", read_only=True)

    
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['user']             

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.name', read_only=True)
    event_price = serializers.SerializerMethodField()
    seat_type = serializers.CharField()
    qr_code = serializers.CharField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'event_name', 'event_price', 'seat_type', 'qr_code', 'is_active']
        
    def get_event_price(self, obj):
        seat = obj.seat_type
        event = obj.event
        if seat == 'Front':
            return event.price_front
        elif seat == 'Behind Goal':
            return event.price_behind_goal
        elif seat == 'Home Side':
            return event.price_side_home
        elif seat == 'Away Side':
            return event.price_side_away
        return None


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
        read_only_fields = ['seller', 'price']

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already registered.")]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)  
      
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email', 'password', ]
        
 

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