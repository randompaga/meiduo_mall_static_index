import re
from django_redis import get_redis_connection

from rest_framework import serializers
from users.models import User
# serializers.ModelSerializer
# serializers.Serializer

"""
用户名,手机号,密码,确认密码,短信验证码,是否同意协议
"""
# 你课下写序列化器的时候 直接从我的笔记里 把代码赋值过来,不要按照我上课的思路自己写
class RegisterUserSerializer(serializers.ModelSerializer):

    password2=serializers.CharField(max_length=20,min_length=8,required=True,label='确认密码')
    sms_code=serializers.CharField(max_length=6,min_length=6,required=True,label='短信验证码')
    allow=serializers.CharField(required=True,label='是否同意协议')


    class Meta:
        model = User
        fields = ['username','mobile','password','allow','password2','sms_code']

    """
    ModelSerializer 自动生成 字段的原理是:
    根据 fields 中的字段,先到当前序列化中查询是否有自己实现的字段,
    如果有就不去模型中自动生成了
    如果没有,则去模型中查找,是否有一致对应的字段,有则生成,没有则报错

    """

    """
    验证数据:
        1.字段类型
        2.字段选项
        3.单个字段
        4.多个字段
    """

    #单个字段校验 手机号格式,是否同意协议
    def validate_mobile(self,value):

        #校验手机号
        if not re.match(r'1[3-9]\d{9}',value):
            raise serializers.ValidationError('手机号不满足规则')

        return value

    def validate_allow(self,value):

        if value != 'true':
            raise serializers.ValidationError('您未同意协议')

        return value
    #多个字段校验 密码和确认密码,短信验证码
    # def validate(self, data):
    def validate(self, attrs):

        #1.密码和确认密码
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError('密码不一致')

        # 2.短信验证码
        # 2.1 用户提交的短信
        sms_code = attrs.get('sms_code')
        #2.2 获取redis的短信
        #① 连接redis
        redis_conn = get_redis_connection('code')
        # ② 获取数据
        mobile = attrs.get('mobile')
        redis_code = redis_conn.get('sms_%s'%mobile)
        # ③ 判断数据是否存在(有有效期)
        if redis_code is None:
            raise serializers.ValidationError('短信验证码已过期')
        #2.3 比对
        if redis_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码输入错误')

        return attrs


    def create(self, validated_data):

        del validated_data['sms_code']
        del validated_data['allow']
        del validated_data['password2']

        user = User.objects.create(**validated_data)

        return user
