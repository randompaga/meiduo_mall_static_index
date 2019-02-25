from users.utils import generate_verify_url
from django.core.mail import send_mail
from celery_tasks.main import app

# name 就是给任务设置一个名字
@app.task(name='send_active_email')
def send_active_email(email,id):

    # send_mail(subject, message, from_email, recipient_list,)
    # subject,          主题
    subject = '美多商场激活邮件'
    # message,          内容
    message = ''
    # from_email,       谁发送的
    # 谁发送的
    from_email = 'qi_rui_hua@163.com'
    # recipient_list    收件人列表
    recipient_list = [email]

    # 生成一个激活的url
    verify_url = generate_verify_url(id, email)

    # from mall import settings
    # from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    #
    # s = Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
    #
    # token = s.dumps({'id':instance.id,'email':email})
    #
    #
    # verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=%s'%token.decode()


    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)

    send_mail(subject, message, from_email, recipient_list,
              html_message=html_message)