from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

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

class OauthQQURLAPIView(APIView):

    def get(self,request):

        return Response({"auth_url":"https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=101474184&redirect_uri=http://www.meiduo.site:8080/oauth_callback.html&state=test"})

