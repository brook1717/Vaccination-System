from django.urls import path
from vaccination import views

app_name = "vaccination"

urlpatterns = [
    path("book/<int:slot_id>/", views.book_slot, name="book-slot"),
    path("booking-success/<int:slot_id>/", views.booking_success, name="booking-success"),
]
