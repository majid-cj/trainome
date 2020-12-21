from rest_framework import serializers
from .models import *


class HomeMenuAPISerializers(serializers.ModelSerializer):
    class Meta:
        model = HomeMenu
        fields = ['pk', 'menu_name', 'menu_url', 'menu_priority', 'menu_logo']

    def create(self, validated_data):
        return HomeMenu.objects.create(**validated_data)


class HomeMenuPermissionAPISerializers(serializers.ModelSerializer):
    menu = HomeMenuAPISerializers(read_only=True)

    class Meta:
        model = HomeMenuPermission
        fields = ['pk', 'member_type', 'menu']

    def create(self, validated_data):
        return HomeMenuPermission.objects.create(**validated_data)
