
from django.conf.urls import url
from .views import OauthQQURLAPIView

urlpatterns = [

    # /oauth/qq/statues/

    url(r'^qq/statues/$',OauthQQURLAPIView.as_view()),
]