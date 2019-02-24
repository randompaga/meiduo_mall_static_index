# jwt_response_payload_handler 系统的方法
# token 就是登陆之后,返回的token
# user 就是认证之后的user
#
import re

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username':user.username,
        'user_id':user.id
    }


from django.contrib.auth.backends import ModelBackend


class UsernameMobileModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        # 1.根据用户名/手机号查询用户
        #  需要区分用户名和手机号
        try:
            if re.match(r'1[3-9]\d{9}',username):
                # 根据正则来判断 用户名 /手机号
                #手机号
                user = User.objects.get(mobile=username)
            else:
                #用户名
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        #2.判断密码
        if user is not None and user.check_password(password):
            return user

        return None


