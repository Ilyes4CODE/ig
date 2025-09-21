# serializers.py
from rest_framework import serializers
from .models import UserLogin, UserSnapshot
import base64
from django.core.files.base import ContentFile

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = ['id', 'username', 'password', 'ip_address', 'user_agent', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class UserSnapshotSerializer(serializers.ModelSerializer):
    image_data = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = UserSnapshot
        fields = ['id', 'user_login', 'image', 'image_data', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'image']
    
    def create(self, validated_data):
        image_data = validated_data.pop('image_data', None)
        snapshot = UserSnapshot.objects.create(user_login=validated_data['user_login'])
        
        if image_data:
            # Remove data URL prefix if present
            if 'data:image' in image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
            else:
                imgstr = image_data
                ext = 'png'
            
            try:
                # Decode base64 image
                import uuid
                data = ContentFile(base64.b64decode(imgstr))
                filename = f"snapshot_{uuid.uuid4()}.{ext}"
                snapshot.image.save(filename, data, save=True)
            except Exception as e:
                print(f"Error saving image: {e}")
        
        return snapshot