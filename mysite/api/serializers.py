from rest_framework import serializers
from vaccine.models import Vaccine
from center.models import Center, Storage


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = [
            "id",
            "name",
            "description",
            "number_of_doses",
            "interval",
            "storage_temperature",
            "minimum_age",
        ]


class StorageSerializer(serializers.ModelSerializer):
    vaccine_name = serializers.CharField(source="vaccine.name", read_only=True)
    available_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Storage
        fields = [
            "id",
            "vaccine",
            "vaccine_name",
            "total_quantity",
            "booked_quantity",
            "available_quantity",
        ]

    def get_available_quantity(self, obj):
        return obj.total_quantity - obj.booked_quantity


class CenterSerializer(serializers.ModelSerializer):
    stock = StorageSerializer(source="storage_set", many=True, read_only=True)

    class Meta:
        model = Center
        fields = [
            "id",
            "name",
            "address",
            "stock",
        ]
