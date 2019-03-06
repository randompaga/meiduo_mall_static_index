import base64
import pickle

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.serializers import CartSerializer, CartSKUSerializer, CartDeleteSerializer
from goods.models import SKU


class CartAPIView(APIView):
    def perform_authentication(self, request):
        pass
    def post(self,request):
        data = request.data
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.validated_data.get('sku_id')
        count = serializer.validated_data.get('count')
        selected = serializer.validated_data.get('selected')
        try:
            user = request.user
        except Exception:
            user = None


        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            redis_conn.hset('cart_%s'%user.id,sku_id,count)
            if selected:
                redis_conn.sadd('cart_selected_%s'%user.id,sku_id)
            return Response(serializer.data)
        else:
            cookie_str = request.COOKIES.get('cart')
            print(type(cookie_str))
            if cookie_str is not None:


                cookie_cart = pickle.loads(base64.b64decode(cookie_str.encode()))


            else:
                cookie_cart ={}
            if sku_id in cookie_cart:
                original_count = cookie_cart[sku_id]['count']
                count+= original_count
            cookie_cart[sku_id]={
                'count':count,
                'selected':selected,
            }
            # 字符串编码成二进制
            bytes_dumps = pickle.dumps(cookie_cart)
            # 编码成b64
            bytes_str = base64.b64encode(bytes_dumps)
            # 解码成字符串
            cookie_save_str = bytes_str.decode()
            response = Response(serializer.data)
            response.set_cookie('cart',cookie_save_str)
            return response

    def get(self,request):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            redis_cart = redis_conn.hgetall('cart_%s'%user.id)
            redis_cart_select = redis_conn.smembers('cart_selected_%s'%user.id)
            cart ={}
            for sku_id,count in redis_cart.items():
                cart[int(sku_id)]={
                    'count':int(count),
                    'selected':sku_id in redis_cart_select
                }
        else:
            cart_str = request.COOKIES.get('cart')

            if cart_str is not None:

                cart = pickle.loads(base64.b64decode(cart_str.encode()))


            else:
                cart={}
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku.count = cart[sku.id]['count']
            sku.selected = cart[sku.id]['selected']

        serializer = CartSKUSerializer(skus,many=True)
        return Response(serializer.data)

    def put(self,request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.data.get('sku_id')
        count = serializer.data.get('count')
        selected = serializer.data.get('selected')
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            redis_conn.hset('cart_%s'%user.id,sku_id,count)
            if selected:
                redis_conn.sadd('cart_selected_%s' % user.id, sku_id)
            else:
                redis_conn.srem('cart_selected_%s' % user.id, sku_id)
            return Response(serializer.data)

        else:
            cookie_str = request.COOKIES.get('cart')
            if cookie_str is not None:

                cookie_cart = pickle.loads(base64.b64decode(cookie_str))
            else:
                cookie_cart = {}

            if sku_id in cookie_cart:
                cookie_cart[sku_id]={
                    'count':count,
                    'selected':selected,
                }

            cookie_save_str=base64.b16encode(pickle.dumps(cookie_cart))
            response = Response(serializer.data)
            response.set_cookie('cart',cookie_save_str,3600)
            return response

    def delete(self,request):
        data = request.data
        serializer = CartDeleteSerializer(data=data)
        serializer.is_valid()
        sku_id = serializer.data.get('sku_id')
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            redis_cart = redis_conn.hdel('cart_%s'%user.id,sku_id)
            # 当点击删除的时候，到redis_cart中把相应的商品id 给删了
            redis_cart = redis_conn.srem('cart_selected_%s'%user.id,sku_id)
            return Response(serializer.data)

        else:
            cart_str = request.COOKIES.get('cart')
            if cart_str is not None:

                cart = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart={}

            response = Response(serializer.data)

            if sku_id in cart:
                del cart[sku_id]
                cookie_str = base64.b64encode(pickle.dumps(cart)).decode()
                response.set_cookie('cart',cookie_str)

            return response












