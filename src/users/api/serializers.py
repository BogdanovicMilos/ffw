from rest_framework import serializers
from users.models import User


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True)
    password = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_email(value):
        if value == '':
            raise serializers.ValidationError("Email cannot be empty.", code=400)
        return value

    @staticmethod
    def validate_password(value):
        if value == '':
            raise serializers.ValidationError("Password cannot be empty.", code=400)
        return value


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )