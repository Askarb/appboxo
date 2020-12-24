from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from apps.accounts.authentication import JWTAuthentication


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserUpdateSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    user = UserSerializer(read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Username or password invalid.')

        jwt_token = JWTAuthentication().generate_token(user)
        return {
            'user': user,
            'token': jwt_token
        }
