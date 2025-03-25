from django.contrib import admin
from .models import Event, Signup, Waitlist

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'current_attendees', 'max_attendees', 'created_at')
    search_fields = ('title',)

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created_at')
    search_fields = ('event__title', 'user__username')

@admin.register(Waitlist)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created_at')
    search_fields = ('event__title', 'user__username')

