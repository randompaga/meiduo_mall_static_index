from decimal import Decimal

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from orders.serializers import OrderSettlementSerializer, OrderCommitSerializer


class OrderSettlementView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        redis_conn = get_redis_connection('cart')
        redis_cart = redis_conn.hgetall('cart_%s'%user.id)
        cart_selected = redis_conn.smembers('cart_selected%s'%user.id)

        cart={}
        # 只有在cart_selected里的sku_id才会被遍历出并被处理
        for sku_id in cart_selected:
            # redis 里存储的count，给新的列表cart
            cart[int(sku_id)]=int(redis_cart[sku_id])

        skus = SKU.objects.filter(id__in = cart.keys())
        for sku in skus:
            # 为什么这里是这么写
            sku.count= cart[sku.id]

        freight = Decimal('10.00')

        serializer = OrderSettlementSerializer({'freight':freight,'skus':skus})
        return Response(serializer.data)


class OrderView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCommitSerializer


