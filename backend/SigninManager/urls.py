from django.urls import path
from .views import GenerateQRCodeAPI, CheckInAPI, CreateEventAPI

urlpatterns = [
    path('<int:event_id>/generate-qr/', GenerateQRCodeAPI.as_view(), name='generate-qr'),
    path('checkin/', CheckInAPI.as_view(), name='checkin'),
    path('events/create/', CreateEventAPI.as_view()),
]
