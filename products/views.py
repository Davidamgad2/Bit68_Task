from rest_framework import viewsets
from . import serializers
from . import models
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
import json
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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
    """Handling getting the products ordered by the price"""
    queryset = models.Product.objects.all().values(
        "id", "name", "price").order_by('price')
    return Response(queryset)


@api_view(['GET'])
def product_search(request):
    """Handling the search process with the name and order it by the price"""
    products = models.Product.objects.all().values("name", "price").filter(
        name__contains=request.GET.get('search')).order_by('price')
    if products:
        return Response(products)
    else:
        return Response({'Message': 'Not Found!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def get_cart(request):
    """Handling getting the cart for the user after adding items"""
    cart = None
    cartitems = []
    cart = models.Cart.objects.get_or_create(
        user=request.user, is_completed=False)[0]
    cartitems = cart.cartitems.all().values("product_id", "quantity")

    return Response(cartitems)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def add_to_cart(request):
    """Handling adding the item to the cart """
    data = json.loads(request.body)
    product = models.Product.objects.get(id=data["id"])

    cart = models.Cart.objects.get_or_create(
        user=request.user, is_completed=False)[0]
    cartitem = models.CartItem.objects.get_or_create(
        cart=cart, product=product)[0]
    try:
        cartitem.quantity += int(data["quantity"])
    except:
        cartitem.quantity += 1

    cartitem.save()
    return Response({'Message': 'Done!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def place_order(request):
    """Handling place new order"""
    new_order = models.Order()
    new_order.user = request.user
    cart = models.Cart.objects.get(user=request.user, is_completed=False)
    cart.is_completed = True
    cartitems = models.CartItem.objects.filter(cart=cart)
    if len(cartitems) == 0:
        return Response({'message': 'You don\'t have anything in cart'})
    cart_total_price = 0
    for item in cartitems:
        cart_total_price += (item.product.price*item.quantity)
    new_order.total_price = cart_total_price
    new_order.save()

    new_order_items = models.CartItem.objects.filter(cart=cart)
    for item in new_order_items:
        models.OrderItem.objects.create(
            order=new_order,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity,
        )

    models.Cart.objects.filter(user=request.user).delete()
    return Response({'message': 'Order added!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def get_order(request):
    """Handling getting all of the orders"""
    orderitems = []
    index = 0
    orders = models.Order.objects.all().filter(user=request.user)
    for counter in orders:
        first = models.Order.objects.all().filter(user=request.user).values(
            "user_id", "total_price", "created_at", "status")[index]
        orderitems.append({'status': first["status"],
                           "created_at": first["created_at"],
                           "user_id": first["user_id"],
                           'total_price': first["total_price"],
                           "products": counter.troll.all().values(
            "order_id", 'product_id', 'price', 'quantity')})
        index += 1
    return Response(orderitems)
