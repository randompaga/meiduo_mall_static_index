from django.shortcuts import render

# Create your views here.

"""
为什么要用静态化
    1. 首页访问是最频繁的
    2. 如果采用原有的方式:
        ① 查询数据库
        ② 将数据动态填充到html中
        会大大降低性能以及用户体验


    问题:
         经常查询数据库,对数据库压力比较大
         将数据动态填充到html中影响用户的体验
    解决:
        ① 针对于 经常查询的数据 可以做缓存处理
        针对与 第二个问题,我们作为后端,没有特别直接的解决方案
        ② 我们把 数据查询出来,然后填充好了,再让用户访问


静态化
     当用户访问我们的页面的时候,我们已经提前准备好了html页面,让用户直接访问就可以了


步骤:
    1.数据查询出来
    2.填充模板
    3.保存到指定的目录


"""

# from fdfs_client.client import Fdfs_client
# client = Fdfs_client('utils/fastdfs/client.conf')
# client.upload_appender_by_file('/home/python/Desktop/images/timg.jpg')


