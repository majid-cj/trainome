from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from .models import Member
from rest_framework.authtoken.models import Token


class MemberSerializers(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['pk', 'email', 'first_name', 'last_name', 'password', 'member_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return Member.objects.create_user(
            validated_data['first_name'], validated_data['last_name'], validated_data['email'], validated_data['password']
        )



class MemberAPISerializers(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['pk', 'email', 'first_name', 'last_name', 'member_type']


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key', ]


class UpdatePassWordSerializers(serializers.Serializer):
    model = Member

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UpdatePassWordSerializers(serializers.Serializer):
    model = Member
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(_("passwords didn't match"))
        return data
