from rest_framework import serializers
from .models import usuarios_atlas
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UsuarioSerializers(serializers.ModelSerializer):
    class Meta:
        model = usuarios_atlas
        fields=("id", "name", "edad", "token")

class CurrentUserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("id",'username', 'password')
