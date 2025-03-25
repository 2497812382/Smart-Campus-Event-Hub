from django.urls import path
from .views import EventCreateView, SignupView, WaitlistView, EventDetailView

urlpatterns = [
    path('events/', EventCreateView.as_view(), name='event-create'),
    path('events/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:event_id>/signup/', SignupView.as_view(), name='event-signup'),
    path('events/<int:event_id>/waitlist/', WaitlistView.as_view(), name='event-waitlist'),
]
