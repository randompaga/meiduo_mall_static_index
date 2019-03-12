from alipay import AliPay
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mall import settings
from orders.models import OrderInfo
class PaymentView(APIView):
    def get(self,request,order_id):
        user = request.user
        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                         user=user,
                                         status = OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return Response({'message':'订单信息有误'},status=status.HTTP_400_BAD_REQUEST)
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            sign_type='RSA2',  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG
        )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),  # 将浮点数转换为字符串
            subject='测试订单',
            return_url='http://www.meiduo.site:8080/pay_success.html',
        )
        # 构造支付地址
        alipay_url = settings.ALIPAY_URL + '?' + order_string
        # 返回响应
        return Response({'alipay_url': alipay_url})