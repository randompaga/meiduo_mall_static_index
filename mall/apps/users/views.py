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
from rest_framework.generics import GenericAPIView
# class RegisterUsernameAPIView(APIView):
class RegisterUsernameAPIView(GenericAPIView):

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
    CreateAPIView                   : 连http请求方法都不用写

五.编码

"""
from users.serializers import RegisterUserSerializer
#############################一级视图##########################################
# class RegisterUserAPIView(APIView):
#
#     def post(self,request):
#         # 1.接收数据
#         data = request.data
#         # 2.校验数据
#         serializer = RegisterUserSerializer(data=data)
#         serializer.is_valid()
#         # 3.数据入库
#         serializer.save()
#         # 4.返回相应
#         # serializer.data
#         # 当我们把模型赋值给序列化器之后, 调用序列化器的 序列化方法(serializer.data 将对象转换为字典)
#         # 原理是: 序列化器根据字段来获取模型中的数据
#
#         return Response(serializer.data)

#############################二级视图##########################################
# from rest_framework.mixins import CreateModelMixin
# class RegisterUserAPIView(CreateModelMixin,GenericAPIView):
#
#     serializer_class = RegisterUserSerializer
#
#     def post(self,request):
#
#         return self.create(request)

#############################三级视图##########################################
from rest_framework.generics import CreateAPIView
class RegisterUserAPIView(CreateAPIView):

    serializer_class = RegisterUserSerializer




