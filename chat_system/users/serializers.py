from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 
                  'username', 
                  'first_name', 
                  'last_name', 
                  'bio', 
                  'date_of_birth', 
                  'email',
                  'phone',
                  'is_active',
                  'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/password-reset/{user.pk}/{token}/"
        send_mail(
            'Password Reset',
            f'Click the link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(pk=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user.")
        
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid token.")

        return data

    def save(self):
        user = User.objects.get(pk=self.validated_data['user_id'])
        user.set_password(self.validated_data['new_password'])
        user.save()


class EmailVerificationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(pk=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user.")
        
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid token.")

        return data

    def save(self):
        user = User.objects.get(pk=self.validated_data['user_id'])
        user.is_active = True
        user.save()