from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from verifications.constants import SMSIMAGE_EXPIRE_TIME

"""
一.分析需求(你要干什么)
二.步骤(大概的思路 你怎么干 前端给你什么,你给前端什么)
三.确定请求方式和路由
四.选取哪个视图(结合需求,使用排除法)
五.编码
"""

"""
一.分析需求
前端将自己生成的uuid 发送给后端,后端生成一个图片验证码给前端就可以了
二.步骤(大概的思路)
    1.后端接收uuid
    2.生成图片验证码
    3.将图片验证码内容保存在redis中
    4.返回图片验证码
三.确定请求方式和路由
    GET     /verifications/imagecodes/(?P<image_code_id>.+)/
四.选取哪个视图(结合需求,使用排除法)
     APIView                         :基类
    GenericAPIView                  :对列表视图和详情视图做了通用支持,一般和mixin配合使用
    ListAPIView,RetrieveAPIView     : 连http请求方法都不用写

五.编码

"""
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection

class RegisterSmsCodeAPIView(APIView):

    def get(self,request,image_code_id):
        # 1.后端接收uuid
        # 2.生成图片验证码
        text,image = captcha.generate_captcha()
        # 3.将图片验证码内容保存在redis中

        #3.1 连接redis
        redis_conn = get_redis_connection('code')
        #3.2 保存数据
        # redis_conn.setex(key,expire,value)
        # redis_conn.setex('img_'+image_code_id,60,text)

        redis_conn.setex('img_%s'%image_code_id,SMSIMAGE_EXPIRE_TIME,text)

        # 4.返回图片验证码
        return HttpResponse(image,content_type='image/jpeg')    #正确

        # 错误的
        # return HttpResponse(image)
        # return Response(image,content_type='image/jpeg')
