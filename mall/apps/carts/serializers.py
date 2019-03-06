from rest_framework import serializers

from goods.models import SKU


class CartSerializer(serializers.Serializer):
    sku_id = serializers.IntegerField(label='商品id', required=True, min_value=0)
    count = serializers.IntegerField(label='个数', required=True, min_value=1)
    selected = serializers.BooleanField(label='是否选中', required=False, default=True)


    def validate(self, attrs):
        sku_id = attrs.get('sku_id')
        try:
            sku = SKU.objects.get(pk=sku_id)
        except SKU.DoseNotExist:
            raise serializers.ValidationError('商品不存在')
        count = attrs.get('count')
        if sku.stock<count:
            raise serializers.ValidationError('商品库存不足')

        return attrs


from rest_framework import serializers
from goods.models import SKU

class CartSKUSerializer(serializers.ModelSerializer):

    count = serializers.IntegerField(label='数量')
    selected = serializers.BooleanField(label='是否勾选')

    class Meta:
        model = SKU
        fields = ('id','count', 'name', 'default_image_url', 'price', 'selected')

class CartDeleteSerializer(serializers.Serializer):
    sku_id = serializers.IntegerField(label='商品id', required=True, min_value=0)

    def validate(self, attrs):
        # sku_id = attrs.get('sku_id')
        try:
            sku = SKU.objects.get(pk = attrs['sku_id'])
        except SKU.DoseNotExist:
            raise serializers.ValidationError('商品不存在')

        return attrs


