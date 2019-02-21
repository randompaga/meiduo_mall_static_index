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