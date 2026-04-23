from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path("vaccines/", views.VaccineListAPI.as_view(), name="vaccine-list"),
    path("vaccines/<int:pk>/", views.VaccineDetailAPI.as_view(), name="vaccine-detail"),
    path("centers/", views.CenterListAPI.as_view(), name="center-list"),
    path("centers/<int:pk>/", views.CenterDetailAPI.as_view(), name="center-detail"),
]
