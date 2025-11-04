from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Ticket, Transfer, Profile
import random
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', "is_active"]
        read_only_fields = ['username']
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["verification_code"]        

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