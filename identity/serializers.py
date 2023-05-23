from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Account


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
