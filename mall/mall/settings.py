"""
Django settings for mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
# git的路径 直接pull 就可以
# https://gitee.com/itcastitheima/meiduo_37.git

# tel:18310820688
# mail: qiruihua@itcast.cn/qiruihua@live.cn
# qq:2860798672

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c*xu*gd8hdpa$8m2u#kcu3y(_e-i&ea#&m^6@7z-fys1e!y1!m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# 我们家 有大门,有后门,还有窗口
# 默认只允许 大门进入    ALLOWED_HOSTS = []

# ALLOWED_HOSTS = [ 大门,后门 ]

#允许我们以什么 来访问后台,这个是一种安全机制
ALLOWED_HOSTS = ['api.meiduo.site','127.0.0.1']


# #跨域访问第三步,设置白名单, 白名单就是允许谁访问
CORS_ORIGIN_WHITELIST  =  (
    '127.0.0.1:8080',
    'localhost:8080',
    'www.meiduo.site:8080'
)
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True




# Application definition

"""
因为我们的子应用 已经放置到apps的包中,这个时候,我们可以通过
配置来告知系统 去哪里查找我们的子应用

'users.apps.UsersConfig', 我们只需要和以前一样 直接写子应用的名字就可以了
不用像 apps.users.apps.UsersConfig 这样写
因为 我们已经 添加了自应用的查找目录 ,
"""
import sys
# sys.path  列表
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'rest_framework',
    'corsheaders', #跨域访问第一步
    'oauth.apps.OauthConfig',
    'areas.apps.AreasConfig',

    # 只要使用模型就需要注册子应用
]

MIDDLEWARE = [
    # #跨域访问第二步
    # 添加在最上边
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'mysql',  # 数据库用户密码
        'NAME': 'meiduo_mall_37'  # 数据库名字

    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'


TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

#日志

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/meiduo.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'utils.exception.exception_handler',

    #JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 优先采用 JWT认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# 替换系统的User,让系统的User也使用我们的模型类
# key=value
# value的形式为: 子应用名.模型类名
# 只能有一个 .
AUTH_USER_MODEL = 'users.User'


# JWT
import datetime
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    #'rest_framework_jwt.utils.jwt_response_payload_handler',
        'utils.users.jwt_response_payload_handler',

    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}

# 自定义认证后端
AUTHENTICATION_BACKENDS = [
    #'django.contrib.auth.backends.ModelBackend'
    'utils.users.UsernameMobileModelBackend'
]


# QQ登录参数
QQ_CLIENT_ID = '101474184'
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'


# 关于邮件发送相关的
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 邮件服务器
EMAIL_HOST = 'smtp.163.com'
# SMTP的默认端口号是: 25
EMAIL_PORT = 25
#发送邮件的邮箱
EMAIL_HOST_USER = 'qi_rui_hua@163.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = '123456abc'

#收件人看到的发件人
EMAIL_FROM = '美多商城<qi_rui_hua@163.com>'


# DRF扩展 缓存
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}