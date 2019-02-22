# jwt_response_payload_handler 系统的方法
# token 就是登陆之后,返回的token
# user 就是认证之后的user
#
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username':user.username,
        'user_id':user.id
    }