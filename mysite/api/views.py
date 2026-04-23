from rest_framework import generics
from vaccine.models import Vaccine
from center.models import Center
from api.serializers import VaccineSerializer, CenterSerializer


class VaccineListAPI(generics.ListAPIView):
    queryset = Vaccine.objects.all().order_by("name")
    serializer_class = VaccineSerializer


class VaccineDetailAPI(generics.RetrieveAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer


class CenterListAPI(generics.ListAPIView):
    queryset = Center.objects.prefetch_related("storage_set__vaccine").order_by("name")
    serializer_class = CenterSerializer


class CenterDetailAPI(generics.RetrieveAPIView):
    queryset = Center.objects.prefetch_related("storage_set__vaccine")
    serializer_class = CenterSerializer
