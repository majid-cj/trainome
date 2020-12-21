from rest_framework import serializers
from .models import Center


class CenterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = [
            'pk', 'name', 'location', 'map_location', 'logo'
        ]