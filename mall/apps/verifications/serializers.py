from rest_framework import serializers

# serializers.ModelSerializer
# serializers.Serializer

# model
from django_redis import get_redis_connection
class RegisterSmsCodeSerializer(serializers.Serializer):

    text = serializers.CharField(label='图片验证码',max_length=4,min_length=4,required=True)
    image_code_id=serializers.UUIDField(label='uuid')

    """
    1. 字段类型
    2. 字段选项
    3. 单个字段
    4. 多个字段
    """

    def validate(self, attrs):
    # def validate(self, data):
    # data = {text:xxx,image_code_id:xxxx}

        #1. 获取用户提交的数据
        text = attrs.get('text')

        #2.获取redis的数据
        #2.1 连接redis
        redis_conn = get_redis_connection('code')
        #2.2 获取数据
        image_code_id=attrs.get('image_code_id')
        redis_text = redis_conn.get('img_%s'%image_code_id)
        #2.3 需要判断数据是否存在
        if redis_text is None:
            raise serializers.ValidationError('图片验证码以过期')
        #3.比对
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('输入不一致')

        return attrs

