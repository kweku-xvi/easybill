import os, jwt
from .models import User
from .permissions import IsVerified
from .serializers import SignUpSerializer, LoginSerializer, UsersSerializer
from .utils import send_email_verification, password_reset_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


load_dotenv()


def get_user(id:str):
    if User.objects.filter(id=id).exists():
        user = User.objects.get(id=id)
    else:
        return Response(
            {
                'success':False,
                'message':'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND
        )
    return user


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.get(email=serializer.validated_data['email'])
            token = RefreshToken.for_user(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('verify_user')
            absolute_url = f'http://{current_site}{relative_link}?token={token}'
            link = str(absolute_url)
            send_email_verification(email=user.email, first_name=user.first_name, link=link)

            return Response(
                {
                    "success":True,
                    "user":serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "success":False,
                "message":serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def verify_user(request):
    if request.method == 'GET':
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {
                    'success':True,
                    'message':'Email verified successfully'
                }, status=status.HTTP_200_OK
            )
            
        except jwt.ExpiredSignatureError as e:
            return Response(
                {
                    'success':False,
                    'message':'Activation link expired'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as e:
            return Response(
                {
                    'success':False,
                    'message':'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.InvalidTokenError as e:
            return Response(
                {
                    'success':False,
                    'message':'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except user.DoesNotExist as e:
            return Response(
                {
                    'success':False,
                    'message':'User not found'
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )
        

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            tokens = serializer.generate_tokens(serializer.validated_data)

            return Response(
                {
                    'success':True,
                    'message':'Login successful!',
                    'tokens':tokens
                }, status=status.HTTP_200_OK
            )
            
@api_view(['POST'])
def password_reset(request):
    if request.method == 'POST':
        email = request.data.get('email')

        if not email:
            return Response (
                {
                    'success':False,
                    'message':'Email is required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request).domain
            relative_link = reverse('password_reset_confirm')
            absolute_url = f'http://{current_site}{relative_link}?uid={uid}&token={token}'
            link = str(absolute_url)

            password_reset_mail(email=user.email, first_name=user.first_name, link=link)

            return Response(
                {
                    'success':True,
                    'message':'Password reset mail successfully sent.'
                }, status=status.HTTP_200_OK
            )
        except User.DoesNotExist as e:
            return Response (
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response (
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['PATCH'])
def password_reset_confirm(request):
    if request.method == 'POST':
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not uid or not token or not password:
            return Response (
                {
                    'success':False,
                    'message':'All fields are required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(id=uid)

            if not default_token_generator.check_token(user, token):
                return Response(
                    {
                        'success':False,
                        'message':'Invalid token'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(password)
            user.save()

            return Response(
                {
                    'success':True,
                    'message':'Password reset successful'
                }, status=status.HTTP_200_OK
            )
        except User.DoesNotExist as e:
            return Response (
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response (
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
def search_users(request):
    if request.method == 'GET':
        query = request.query_params.get('query')

        if not query:
            return Response(
                {
                    'success':False,
                    'message':'No search query provided'
                }, status=status.HTTP_400_BAD_REQUEST          
            )

        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(business_name__icontains=query)
        )

        serializer = UsersSerializer(results, many=True)

        return Response(
            {
                'success':True,
                'message':'Search results:',
                'users':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_by_id(request, id:str):
    if request.method == 'GET':
        user = get_user(id=id)

        serializer = UsersSerializer(user)

        return Response(
            {
                'success':True,
                'user':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()

        serializer = UsersSerializer(users, many=True)

        return Response(
            {
                'success':True,
                'users':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsVerified])
def update_user_info(request, id:str):
    if request.method == 'PUT' or request.method == 'PATCH':
        current_user = request.user

        user = get_user(id=id)

        if current_user != user and not current_user.is_staff:
            return Response(
                {
                    'success':False,
                    'message':'You do not have thee permission to perform this action'
                }, status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UsersSerializer(user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                {
                    'success':True,
                    'user':serializer.data
                }, status=status.HTTP_200_OK
            )


@api_view(['DELETE'])
@permission_classes({IsVerified})
def delete_user(request, id:str):
    if request.method == 'DELETE':
        current_user = request.user

        user = get_user(id=id)

        if current_user != user and not current_user.is_staff:
            return Response(
                {
                    'success':False,
                    'message':'You do not have thee permission to perform this action'
                }, status=status.HTTP_403_FORBIDDEN
            )
        
        user.delete()

        return Response(
            {
                'success':True,
                'message':'User deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT
        )