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

    password2=serializers.CharField(max_length=20,min_length=8,write_only=True,required=True,label='确认密码')
    sms_code=serializers.CharField(max_length=6,min_length=6,write_only=True,required=True,label='短信验证码')
    allow=serializers.CharField(required=True,write_only=True,label='是否同意协议')

    # token 是在序列化的时候 使用,在反序列化的时候 默认忽略
    # token = serializers.CharField()

    token = serializers.CharField(read_only=True)
    # password

    #write_only	表明该字段仅用于反序列化输入，默认False
    # 在序列化的时候 默认 忽略

    # 以上的三个字段 ,我们的期望只是在验证的时候 传入
    # 我们在进行 序列化(对象转字典)操作的时候,忽略这3个字段('allow','password2','sms_code')


    class Meta:
        model = User
        fields = ['username','mobile','password','allow','token','password2','sms_code']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

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
        # 修改密码
        user.set_password(validated_data.get('password'))
        # 修改完模型的数据之后,要记得保存模型
        user.save()

        # 1.用户注册完成之后
        # 2.生成一个token

        from rest_framework_jwt.settings import api_settings

        #① 获取 jwt的2个方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        #② 将user信息 传递给 payload方法
        payload = jwt_payload_handler(user)

        #③ 对payload返回的数据进行编码,编码之后就是token
        token = jwt_encode_handler(payload)


        # 3.将token返回给前端
        # 让序列化器 来获取token

        user.token = token

        return user


# class Person(object):
#
#     name = 'itcast'
#
# p = Person()
#
# p.name = 'abc'
# p.age = 10
#
# p2 = Person()
# print(p2.age)
