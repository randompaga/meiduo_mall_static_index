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
from rest_framework.mixins import CreateModelMixin

"""
封装(抽取)的原则:
    1.(n行代码)实现了一个小的功能
    2.重复的代码( 部分代码出现了 n次)

封装(抽取)的步骤:
    1. 先定义一个方法(函数)(不要写任何参数)
    2. 将要抽取的代码,放入定义的方法(函数)中,导入必须的一些库,没有(报错)的变量,以参数的形式体现
    3. 测试代码(先把原代码,注释掉,没有问题之后,再删除)
"""

def get_user_by_username(username):
    try:
        if re.match(r'1[3-9]\d{9}', username):
            # 根据正则来判断 用户名 /手机号
            # 手机号
            user = User.objects.get(mobile=username)
        else:
            # 用户名
            user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    return user



class UsernameMobileModelBackend(ModelBackend):



    def authenticate(self, request, username=None, password=None, **kwargs):

        # 1.根据用户名/手机号查询用户
        #  需要区分用户名和手机号
        # try:
        #     if re.match(r'1[3-9]\d{9}',username):
        #         # 根据正则来判断 用户名 /手机号
        #         #手机号
        #         user = User.objects.get(mobile=username)
        #     else:
        #         #用户名
        #         user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     user = None

        user = get_user_by_username(username)

        #2.判断密码
        if user is not None and user.check_password(password):
            return user

        return None


