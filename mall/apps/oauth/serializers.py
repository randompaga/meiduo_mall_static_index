from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.utils import check_access_token
from users.models import User
from .models import OAuthQQUser

# serializers.ModelSerializer
# serializers.Serializer
# 当前 ModelSerializer 没有优势

# access_token(openid), 手机号,密码,短信验证码
#(access_token,短信验证码,判断用户是否存在)
class OauthQQUserSerializer(serializers.Serializer):

    access_token = serializers.CharField(label='操作凭证')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')


    def validate(self, attrs):

        #1. access_token
        access_token = attrs['access_token']

        openid = check_access_token(access_token)

        if openid is None:
            raise serializers.ValidationError('openid过期')

        #将openid添加到 attrs中
        attrs['openid']=openid

        #2.短信验证码
        # 2.短信验证码
        # 2.1 用户提交的短信
        sms_code = attrs.get('sms_code')
        # 2.2 获取redis的短信
        # ① 连接redis
        redis_conn = get_redis_connection('code')
        # ② 获取数据
        mobile = attrs.get('mobile')
        redis_code = redis_conn.get('sms_%s' % mobile)
        # ③ 判断数据是否存在(有有效期)
        if redis_code is None:
            raise serializers.ValidationError('短信验证码已过期')
        # 2.3 比对
        if redis_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码输入错误')

        #3.判断用户
        # mobile
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            #说明 该手机号没有注册过
            #就应该创建一个用户
            # validate 方法主要是为了 进行 数据的验证,创建用户的代码
            # 我们写在后边
            pass
        else:
            #说明 注册过
            # 注册过就要验证密码是否正确
            password = attrs['password']
            if not user.check_password(password):
                raise serializers.ValidationError('密码不正确')

            attrs['user']=user


        return attrs

    # data --> attrs --> validated_data
    def create(self, validated_data):

        user = validated_data.get('user')

        if user is None:
            #说明手机号没有注册过
            user = User.objects.create(
                username=validated_data.get('mobile'),
                mobile=validated_data.get('mobile'),
                password=validated_data.get('password')
            )

            user.set_password(validated_data.get('password'))
            user.save()


        qquser = OAuthQQUser.objects.create(
            user=user,
            openid=validated_data.get('openid')
        )

        return qquser
