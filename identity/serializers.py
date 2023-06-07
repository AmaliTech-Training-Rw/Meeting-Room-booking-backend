from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Account, PasswordResetToken
from django.core.mail import send_mail
from app import settings


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'organization_name', 'email', 'type_of_organization', 'location', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            organization_name=self.validated_data['organization_name'],
            type_of_organization=self.validated_data['type_of_organization'],
            location=self.validated_data['location']
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            # Get the username and password from the serializer data
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
            # If the credentials are valid, store the user object in the data dictionary
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        User = get_user_model()
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")

        self.user = user
        return value

    def send_reset_email(self, request):
        # print (os.environ.get("EMAIL_USER"))
        token = PasswordResetToken.generate_token(self.user)
        # token = default_token_generator.make_token(self.user)
        reset_url = f"{settings.FRONTEND_URL}/api/account/password-reset/confirm/{token}/"
        subject = "Reset Your Password"
        message = f"Click the link below to reset your password:\n\n{reset_url}"
        send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL, [
                self.user.email])

    def save(self, request):
        self.send_reset_email(request)


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        token = self.context['token']
        user = None
        try:
            user = get_object_or_404(
                get_user_model(),
                passwordresettoken__token=token)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("Invalid or expired token.")

        if user is not None:
            # Additional validation logic if needed
            return data
        return data

    def save(self, token, user):
        user.set_password(self.validated_data['password'])
        user.save()

        PasswordResetToken.objects.filter(user=user, token=token).delete()
