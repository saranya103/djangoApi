from rest_framework import serializers
from .models import User, Book
from allauth.account.utils import setup_user_email
from myproject import settings
from allauth.account.adapter import get_adapter


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data['is_staff'].lower() and validated_data['is_superuser'].lower() == "true":
            user = User.objects.create_superuser(
                validated_data['username'], validated_data['email'], validated_data['password'])

        else:
            user = User.objects.create_user(
                validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'bookname', 'bookstatus']
