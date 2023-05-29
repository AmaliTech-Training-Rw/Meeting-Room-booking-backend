from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import logout
from .serializers import RegistrationSerializer, LoginSerializer
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
