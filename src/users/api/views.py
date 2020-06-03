import requests
from django.db.models import Q
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import LoginSerializer, RegisterSerializer
from oauth2_provider.views.mixins import OAuthLibMixin

CLIENT_ID = 'jLLymQam7t0O0Va1yIUp7i0SyKb47KOlFlP6BgMN'
CLIENT_SECRET = '0WBKETjXpqBF0yhaMSzEXk3io25ZmsIJQVgYchwWgl0WfmsYZv7TfiF5Sbq0q8sbkQKHoF2rSR4eJKqf1igNyo0qE82J1m54WkLhkAR8YlgCkFLcxP6Ib2hQYgmyvOMm'


class SignIn(OAuthLibMixin, APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'success': False, 'error': 'You are already authenticated', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            obj = User.objects.filter(Q(email__iexact=serializer.validated_data['email'])).distinct()
            if obj.exists() and obj.count() == 1:
                user = obj.first()
                print(user)
                if user.check_password(serializer.validated_data['password']):
                    r = requests.post('http://127.0.0.1:6767/o/token/',
                        data={
                            'grant_type': 'password',
                            'username': serializer.validated_data['email'],
                            'password': serializer.validated_data['password'],
                            'client_id': CLIENT_ID,
                            'client_secret': CLIENT_SECRET,
                        },
                    )
                    return Response({'success': True, 'message': 'Logged in successfully', 'data': r.json()}, status=status.HTTP_200_OK)
                return Response({'success': False, 'error': 'Invalid credentials', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success': False, 'error': 'User does not exist', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': False, 'error': 'Could not login with provided information', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)


class SignUp(OAuthLibMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'success': False, 'error': 'You are already authenticated', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            obj = User.objects.filter(Q(email__iexact=serializer.validated_data['email'])).distinct()
            if obj.exists() and obj.count() == 1:
                return Response({'success': False, 'error': 'User already registered', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({'success': True, 'message': 'Registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'All fields are required', 'error': serializer.errors, 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
