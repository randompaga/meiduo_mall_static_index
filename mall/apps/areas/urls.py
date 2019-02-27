from django.conf.urls import url
from .views import ProvienceAPIView,DistrictAPIView


urlpatterns = [

    #省 areas/infos
    url(r'^infos/$',ProvienceAPIView.as_view()),
    url(r'^infos/(?P<id>\d+)/$',DistrictAPIView.as_view()),
]