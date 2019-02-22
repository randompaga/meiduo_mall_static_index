from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    #/users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameAPIView.as_view(),name='usernamecount'),

    url(r'^$',views.RegisterUserAPIView.as_view()),

    # 我们登陆的url 采用
    # users/auths/

    url(r'^auths/',obtain_jwt_token),
    # url(r'^api-token-auth/',obtain_jwt_token),
]

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
#eyJ1c2VyX2lkIjoxMCwiZW1haWwiOiIiLCJ1c2VybmFtZSI6Iml0Y2FzdCIsImV4cCI6MTU1MDgyNDAxOX0.
#c4errq2huCv9VcSh4MWWpAEFcC-tH_eiCigZld6me5A
