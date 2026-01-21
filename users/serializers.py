from rest_framework import serializers
from users.models import User
from django.contrib.auth import get_user_model

customUser = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.Role.choices)
    class Meta:
        model = customUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
        }
        validators = {
            'username': {
                'unique': True,
            },
            'email': {
                'unique': True,
            }
        }
        def create(self, validated_data):
            user = customUser.objects.create_user(**validated_data)
            return user
        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.save()
            return instance
        def validate_username(self, value):
            if len(value) < 5:
                raise serializers.ValidationError('Username must be at least 5 characters long.')
            return value
        def validate_email(self, value):
            if not '@' in value:
                raise serializers.ValidationError('Email must contain a valid domain.')
            return value
        def validate_password(self, value):
            if len(value) < 8:
                raise serializers.ValidationError('Password must be at least 8 characters long.')
            return value
        def validate_role(self, value):
            if value not in User.Role.choices:
                raise serializers.ValidationError('Invalid role.')
            return value
        
