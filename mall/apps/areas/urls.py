from django.conf.urls import url
from .views import ProvienceAPIView,DistrictAPIView,AreaModelViewSet


urlpatterns = [

    #省 areas/infos
    # url(r'^infos/$',ProvienceAPIView.as_view()),
    # url(r'^infos/(?P<id>\d+)/$',DistrictAPIView.as_view()),
]

from rest_framework.routers import DefaultRouter

#1.创建router
router = DefaultRouter()

#2.注册路由
router.register(r'infos',AreaModelViewSet,base_name='area')

#3.将router自动生成的url 添加到urlpatterns
urlpatterns += router.urls

