from rest_framework import serializers

from teachbase.models import Course, CustomUser


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        return course


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        course = CustomUser.objects.create(**validated_data)
        return course
