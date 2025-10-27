from django.db import models
from django.contrib.auth.models import User
# create first model
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

#Create 2nd model 
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #Link it with user
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    qr_code = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.event.name} - {self.user.username}"

# create third model
class Transfer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='sales', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of {self.ticket} by {self.seller}"
