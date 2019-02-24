from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mall import settings
def generate_openid_token(openid):

    #1.创建序列化器
    s = Serializer(secret_key=settings.SECRET_KEY,expires_in=60*10)
    #2.组织数据
    data = {
        'openid':openid
    }
    #3.加密
    token  = s.dumps(data)

    #返回字符串
    return token.decode()
