from .models import Customer
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_number', 'added_by']

        read_only_fields = ['id', 'added_by']

    def get_added_by(self, obj):
        return obj.added_by.username if obj.added_by else None