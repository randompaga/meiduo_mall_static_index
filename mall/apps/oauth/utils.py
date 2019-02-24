from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired,BadSignature
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

def check_access_token(token):

    #1. 创建序列化器
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=60 * 10)
    #2.解密 (会有可能存在异常)
    try:
        result = s.loads(token)
        # 如果数据没问题 data = {}
    # except SignatureExpired:
    #     pass
    except BadSignature:
        #说明数据有问题,返回None
        return None
    #3.返回数据
    return result.get('openid')


