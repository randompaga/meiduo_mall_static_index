from decimal import Decimal
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import serializers

from goods.models import SKU


class CartSKUSerializer(serializers.ModelSerializer):
    """
    购物车商品数据序列化器
    """
    count = serializers.IntegerField(label='数量')

    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image_url', 'price', 'count')


class OrderSettlementSerializer(serializers.Serializer):
    """
    订单结算数据序列化器
    """
    freight = serializers.DecimalField(label='运费', max_digits=10, decimal_places=2)
    skus = CartSKUSerializer(many=True)


from orders.models import OrderInfo, OrderGoods

class PlaceOrderSerialzier(serializers.Serializer):

    freight = serializers.DecimalField(label='运费',decimal_places=2,max_digits=10)
    skus = CartSKUSerializer(many=True)

class OrderCommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'address', 'pay_method')
        read_only_fields = ('order_id',)
        extra_kwargs = {
            'address': {
                'write_only': True,
                'required': True,
            },
            'pay_method': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data):
        """保存订单"""
        user = self.context['request'].user
        order_id = timezone.now().strftime('%Y%M%D%H%M%S')+('%09d'%user.id)
        address = validated_data['address']
        pay_method = validated_data['pay_method']
        # 这一堆啥玩意？
        order = OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=0,
            total_amount=Decimal('0'),
            freight=Decimal('10.0'),
            pay_method=pay_method,
            status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'] if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH'] else
            OrderInfo.ORDER_STATUS_ENUM['UNPAID']
        )

        redis_conn = get_redis_connection('cart')
        cart_redis = redis_conn.hgetall('cart_%s' % user.id)
        cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)
        # 遍历结算商品：
        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(cart_redis[sku_id])

        sku_id_list = cart.keys()

        for sku_id in sku_id_list:
            sku = SKU.objects.get(pk=sku_id)
            count = cart[sku.id]
            if sku.stock < count:
                raise serializers.ValidationError('库存不足')

            sku.stock-=count
            sku.sales+=count
            sku.save()

            order.total_count+=count
            order.total_amount +=(sku.price*count)

            OrderGoods.objects.create(
                order = order,
                sku = sku,
                count =count,
                price = sku.price,
            )
        order.save()

        pl = redis_conn.pipeline()
        pl.hdel('cart_%s'%user.id,*cart_selected)
        pl.srem('cart_selected_%s'%user.id,*cart_selected)
        pl.execute()

        return order




