from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

"""
对于应用而言，需要进行两步：
1. 获取Authorization Code；        其实就是通过 url来得到用户的同意

2. 通过Authorization Code获取Access Token


对于我们来说,
3.通过token 换取openid

"""

"""
https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=101474184&redirect_uri=http://www.meiduo.site:8080/oauth_callback.html&state=test

"""

"""

一.分析需求
    当用户点击qq登陆按钮的时候,发送一个请求就可以,后端返回我们一个url

二.步骤(大概的思路)
    根据qq提供的接口文档 拼接url

三.确定请求方式和路由

    GET
四.选取哪个视图(结合需求,使用排除法)

五.编码
"""

from QQLoginTool.QQtool import OAuthQQ
from mall import settings
class OauthQQURLAPIView(APIView):

    def get(self,request):

        #1.创建 OauthQQ的实例对象
        state = 'test'

        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=state)
        #2.调用实例对象的方法
        auth_url = oauth.get_qq_url()


        return Response({"auth_url":auth_url})

"""
一,需求:
    当用户点击同意之后,qq认证服务器会返回一个code,这个时候,需要让前端将
    code返回给后端

二.思路(步骤)

    1.接收code
    2.通过code换取token
    3.通过token换取openid
    4.
三. 请求方式和路由
    GET     /oauth/qq/users/?code=xxxx

    POST    /oauth/qq/users/        body code:xxxx
四. 确定选择哪个视图
    APIView:
    GenericAPIView:
    ListAPIVIew,RetrieveAPIView:

"""

class QQOauthUserAPIView(APIView):

    def get(self,request):
        # 1.接收code
        # 2.通过code换取token
        # 3.通过token换取openid

        pass