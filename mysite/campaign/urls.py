from django.urls import path
from campaign import views

app_name = "campaign"

urlpatterns = [
    path("", views.campaign_list, name="list"),
    path("<int:id>/", views.campaign_detail, name="detail"),
]
