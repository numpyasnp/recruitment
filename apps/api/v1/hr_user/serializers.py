from rest_framework import serializers
from apps.hr_user.models import HRUser


class HRUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = HRUser
        fields = [
            "id",
            "name",
            "last_name",
            "email",
            "hr_company",
            "client_companies",
            "password",
        ]
        read_only_fields = ["id", "date_joined"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = HRUser.objects.create_user(password=password, **validated_data)
        return user


class HRUserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = HRUser
        fields = [
            "id",
            "name",
            "last_name",
            "email",
            "hr_company",
            "client_companies",
            "password",
        ]
        read_only_fields = ["id", "date_joined"]

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
