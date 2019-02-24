
from django.conf.urls import url
from .views import OauthQQURLAPIView,OauthQQUserAPIView

urlpatterns = [

    # /oauth/qq/statues/

    url(r'^qq/statues/$',OauthQQURLAPIView.as_view()),

    # /oauth/qq/users/?code=xxx
    url(r'^qq/users/$',OauthQQUserAPIView.as_view()),
]