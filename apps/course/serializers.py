from rest_framework import serializers
from .models import *
from apps.center.serializers import CenterSerializers
from apps.accounts.serializers import MemberAPISerializers


class CourseSerializers(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = [
            'pk', 'category', 'center', 'name', 'description', 'cover', 'price',
            'trainee', 'trainee_image', 'discount', 'lectures', 'details', 'add_date'
        ]

    def get_details(self, obj):
        return {
            'view': obj.get_views(),
            'rate': obj.get_rates(),
        }
    
    def to_representation(self, instance):
        self.fields['center'] = CenterSerializers(read_only=True)
        return super(CourseSerializers, self).to_representation(instance)


class CourseRateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseRate
        fields = [
            'course', 'account', 'rate'
        ]


class CourseCommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = CourseComment
        fields = [
            'pk', 'course', 'account', 'comment', 'add_date'
        ]
    
    def to_representation(self, instance):
        self.fields['course'] = CourseSerializers(read_only=True)
        self.fields['account'] = MemberAPISerializers(read_only=True)
        return super(CourseCommentSerializers, self).to_representation(instance)


class LectureSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = [
            'pk', 'course', 'name', 'file', 'duration'
        ]
    
    def to_representation(self, instance):
        self.fields['course'] = CourseSerializers(read_only=True)
        return super(LectureSerializers, self).to_representation(instance)


class CoursePaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoursePayment
        fields = ['pk', 'course', 'account', 'payment', 'phone', 'allow_access', 'add_date']
