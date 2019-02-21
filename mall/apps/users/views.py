from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

# from mall.apps.users.models import User       错误的

# from apps.users.models import User            错误

from users.models import User
from users.serializers import RegisterUserSerializer

"""
一.分析需求
二.步骤(大概的思路)
三.确定请求方式和路由
四.选取哪个视图(结合需求,使用排除法)
五.编码
"""

"""
一.分析需求
当用户在用户名输入框中输入用户之后,当光标移开之后,前端应该 发送一个ajax请求
前端应该将 用户名传递给后端

    判断用户名有没有注册
    count   0       没有注册
    count   1       注册过来

    /users/usernames/itcast/count/

    /users/usernames/(?P<username>\w{5,20})/count/

二. 步骤(大概的思路)
   1. 后端接收数据
   2. 数据验证
   3. 查询数据库
   4. 返回相应

三.确定请求方式和路由
    GET     /users/usernames/(?P<username>\w{5,20})/count/

四.选取哪个视图(结合需求)
    APIView                         :基类
    GenericAPIView                  :对列表视图和详情视图做了通用支持,一般和mixin配合使用
    ListAPIView,RetrieveAPIView     : 连http请求方法都不用写

五.编码

"""
from rest_framework.views import APIView
class RegisterUsernameAPIView(APIView):

    def get(self,request,username):
        # 1. 后端接收数据
        # 2. 数据验证
        # 3. 查询数据库
        count = User.objects.filter(username=username).count()

        data = {
            'count':count,
            'username':username
        }

        # 4. 返回相应
        return Response(data)

"""
一.分析需求
    当用户点击注册按钮的时候,需要让前端收集 用户名,手机号,密码,确认密码,短信验证码,是否同意协议

二.步骤(大概的思路)
    1.接收数据
    2.校验数据
    3.数据入库
    4.返回相应

三.确定请求方式和路由
    POST        users/


四.选取哪个视图(结合需求,使用排除法)
    APIView                         :基类
    GenericAPIView                  :对列表视图和详情视图做了通用支持,一般和mixin配合使用
    CreateAPIView                    : 连http请求方法都不用写

五.编码

"""
from users.serializers import RegisterUserSerializer
class RegisterUserAPIView(APIView):

    def post(self,request):
        # 1.接收数据
        data = request.data
        # 2.校验数据
        serializer = RegisterUserSerializer(data=data)
        serializer.is_valid()
        # 3.数据入库
        serializer.save()
        # 4.返回相应
        return Response(serializer.data)





