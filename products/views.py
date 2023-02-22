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
import json
from rest_framework import status


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
def order_products(request):
    queryset = models.Product.objects.all().values(
        "id", "name", "price").order_by('price')
    return Response(queryset)


@api_view(['GET'])
def product_search(request):
    products = models.Product.objects.all().values("name", "price").filter(
        name__contains=request.GET.get('search')).order_by('price')
    if products:
        return Response(products)
    else:
        return Response({'Message': 'Not Found!'})

@api_view(['GET'])
def get_cart(request):
    """"""
    cart=None
    cartitems=[]
    if request.user.is_authenticated:
        cart=models.Cart.objects.get_or_create(user=request.user,is_completed=False)[0]
        cartitems=cart.cartitems.all().values("product_id","quantity")

    return Response(cartitems)   

    

@api_view(['POST'])
def add_to_cart(request):
    """"""
    data = json.loads(request.body)
    product = models.Product.objects.get(id= data["id"])
    if request.user.is_authenticated:
        cart = models.Cart.objects.get_or_create(user=request.user, is_completed=False)[0]
        cartitem = models.CartItem.objects.get_or_create(cart=cart, product=product)[0]
        try:
            cartitem.quantity+=int(data["quantity"])
        except:
            cartitem.quantity += 1
            
        cartitem.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
