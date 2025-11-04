from django.contrib import admin

from .models import Event, Ticket, Transfer, Profile, Cart

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Transfer)
admin.site.register(Profile)
admin.site.register(Cart)

