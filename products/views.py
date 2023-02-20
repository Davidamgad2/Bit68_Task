from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
    """handle creating and updating profiles """
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.updateownprofile,)
    search_fields = ('name', 'email',)
    
    def get_queryset(self):
        pass


class UserLoginApiView(ObtainAuthToken):
    """handling creating user auth token """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

@api_view(['GET'])
def products_view(request): 
    queryset=models.Product.objects.all().values("name", "price").order_by('price')
    return Response( queryset)
