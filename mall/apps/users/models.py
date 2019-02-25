from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
"""
1. 可以自己定义模型(需要分析字段)
2. 因为django自带了后台用户系统,所以我们可以分析 自带的后台是否可以使用
"""

class User(AbstractUser):


    mobile=models.CharField(verbose_name='手机号',max_length=11,unique=True)

    email_active=models.BooleanField(default=False,verbose_name='邮件激活状态')


    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name  #复数形式