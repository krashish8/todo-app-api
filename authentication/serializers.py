from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials or the user does not exist!")
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError("Email already exists!")
        return email
    
    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError("Username already taken!")
        return username

    def save(self, **kwargs):
        data = self.validated_data
        names = data['name'].split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ""
        email = data['email']
        username = data['username']
        password = data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        """
        Get full name of the logged in user using the
        get_full_name() function of the User model
        """
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username')
    