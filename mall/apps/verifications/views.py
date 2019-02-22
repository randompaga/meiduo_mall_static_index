from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.yuntongxun.sms import CCP
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

from rest_framework import renderers
class JPEGRenderer(renderers.BaseRenderer):
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

class RegisterImageCodeAPIView(APIView):

    renderer_classes = [JPEGRenderer]

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
        # return HttpResponse(image,content_type='image/jpeg')    #正确

        # 错误的
        # return HttpResponse(image)
        return Response(image,content_type='image/jpeg')

"""
一.分析需求(你要干什么)
    当用户点击获取短信验证码的时候,前端应该发送ajax请求,将
    手机号,图片验证码的内容,以及uuid 传递给后端

二.步骤(大概的思路 你怎么干 前端给你什么,你给前端什么)
    1.后端接收数据
    2.校验数据 (数据格式,数据的内容[图片验证码是否正确])
    3.生成一个短信码
    4.发送短信
    5.保存短信
    6.返回相应
三.确定请求方式和路由
    verifications/smscodes/mobile/text/image_code_id/

    verifications/smscodes/?mobile=xxx&text=xxxx&image_code_id=xxxx

    GET   verifications/smscodes/(?P<mobile>1[3-9]\d{9})/?text=xxxx&image_code_id=xxx

    POST  verifications/smscodes/   body

四.选取哪个视图(结合需求,使用排除法)
    APIView                         :基类
    GenericAPIView                  :对列表视图和详情视图做了通用支持,一般和mixin配合使用
    ListAPIView,RetrieveAPIView     : 连http请求方法都不用写

五.编码

"""
from verifications.serializers import RegisterSmsCodeSerializer
class RegisterSmsCodeAPIView(APIView):
    """
     GET   verifications/smscodes/(?P<mobile>1[3-9]\d{9})/?text=xxxx&image_code_id=xxx
    """
    def get(self,request,mobile):
        # 1.后端接收数据
        query_params = request.query_params

        # 2.校验数据 (数据格式,数据的内容[图片验证码是否正确])
        # text = query_params.get('text')
        # image_code_id=query_params.get('image_code_id')

        serializer = RegisterSmsCodeSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)

        # 3.生成一个短信码
        import random
        sms_code = '%06d'%random.randint(0,999999)

        # 4.发送短信
        # CCP().send_template_sms(mobile,[sms_code,5],1)

        from celery_tasks.sms.tasks import send_sms_code

        # send_sms_code(mobile,sms_code)  错误的
        # delay 的参数 同前边函数的参数
        send_sms_code.delay(mobile,sms_code)

        # 5.保存短信
        redis_conn = get_redis_connection('code')

        # redis_conn.setex(key,expire,value)
        redis_conn.setex('sms_%s'%mobile,5*60,sms_code)
        # 6.返回相应
        return Response({'msg':'ok'})



