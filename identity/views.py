from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import logout, get_user_model
from django.shortcuts import get_object_or_404
from .serializers import (RegistrationSerializer, LoginSerializer,
                          PasswordResetSerializer, PasswordResetConfirmSerializer)
# Create your views here.


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user"
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Perform any additional tasks or authentication checks here if needed
            # For example, you can generate a token or session for the authenticated user
            data = {
                'response': 'Login successful',
                'email': user.email,
                'username': user.username
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        # Call Django's logout function to log out the user
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def password_reset_view(request):
    if request.method == 'POST':
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def password_reset_confirm_view(request, token):
    print(request)
    if request.method == 'POST':

        serializer = PasswordResetConfirmSerializer(data=request.data, context={'request': request, 'token': token})

        if serializer.is_valid():
            user_name = get_object_or_404(get_user_model(), passwordresettoken__token=token)
            User = get_user_model()
            user_model = User.objects.get(username=user_name)

            serializer.save(token, user_model)
            return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
