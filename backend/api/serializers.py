from rest_framework import serializers
from users.models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'email_verified', 'created_at']
        read_only_fields = ['id', 'email_verified', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password', None)
        
        # Create user
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Create associated profile
        Profile.objects.create(user=user)
        
        return user

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    tier = serializers.SerializerMethodField()
    is_pro = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'tier', 'is_pro']
        read_only_fields = ['id', 'username', 'email', 'tier', 'is_pro']
    
    def get_tier(self, obj):
        return obj.user.current_tier
    
    def get_is_pro(self, obj):
        return obj.user.is_pro()


class SubmitAnswerSerializer(serializers.Serializer):
    """Serializer for submitting exam answers"""
    attempt_id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)
    selected_option = serializers.ChoiceField(
        choices=['A', 'B', 'C', 'D'],
        required=True,
        allow_blank=False
    )
