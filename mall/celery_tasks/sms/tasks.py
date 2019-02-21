"""
Celery

任务         创建任务
            1.任务的包名(随意) , 包中的文件 必须是 tasks.py
            2.所谓的任务 其实就是函数
            3.这个任务必须被Celery的实例对象的 task装饰器装饰
            4.这个任务,必须要让Celery自动检测
broker
worker
"""
from libs.yuntongxun.sms import CCP
from celery_tasks.main import app

@app.task
def send_sms_code(mobile,sms_code):

    CCP().send_template_sms(mobile, [sms_code, 5], 1)
