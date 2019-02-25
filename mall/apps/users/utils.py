from mall import settings

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def generate_verify_url(id,email):



    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)

    token = s.dumps({'id': id, 'email': email})

    verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=%s' % token.decode()

    return verify_url
