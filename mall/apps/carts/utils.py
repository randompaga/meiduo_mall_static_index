
import base64
import pickle

from django_redis import get_redis_connection

def merge_cookie_to_redis(request,user,response):
    cookie_str = request.COOKIES.get('cart')
    if cookie_str is not None:
        cookie_cart = pickle.loads(base64.b64decode(cookie_str.encode()))
        #cookie_cart
        # {'1':{'count':2,'selected':selected},'2':{'count':3,'selected':selected}}

        redis_conn = get_redis_connection('cart')
        # redis_cart 商品ID（键） 和收藏数量（值）
        redis_cart = redis_conn.hgetall('cart_%s'%user.id)
        # redis_cart:
        # hash:   {sku_id:count}
        cart = {}
        # 遍历取出redis_cart （键） 和（值）
        for sku_id,count in redis_cart.items():
            # 注意redis 里的数据是bytes,需加int转换
            cart[int(sku_id)] = int(count)

        selected_sku_id_list =[]
        # 将cookie里的商品ＩＤ和已经勾选的数量，经过循环遍历取出
        for sku_id,selected_count_dict in cookie_cart.items():
            # sku_id是键，selected_count_dict是值（又是一个字典，count,selected是这个字典里的键）
            # 用cookie里的商品数量覆盖（更新）redis 里的商品数量
            # selected_count_dict['count']取到cookie里的count值
            cart[sku_id] = selected_count_dict['count']
            # 如果selected_count_dict的键'selected'有值，就是'selected'：selected,那么将该值对应的键添加到已选中的商品列表中
            if selected_count_dict['selected']:
                selected_sku_id_list.append(sku_id)

        pl = redis_conn.pipeline()
        # hmset:
        # 同时将多个field - value(域 - 值)对设置到哈希表key中。
        # hmset:
        # 同时将多个field - value(域 - 值)对设置到哈希表key中。
        # 更新过后的cart是个hash:
        pl.hmset('cart_%s'%user.id,cart)
        # 将选中的商品列表拆包作为值和用户一起添加到redis中
        pl.sadd('cart_selected_%s'%user,*selected_sku_id_list)
        pl.execute()

        response.delete_cookie('cart')
        return response
    else:
        return response
'''

import pickle

import base64
from django_redis import get_redis_connection


def merge_cookie_to_redis(request,user,response):

    """
    1.获取cookie数据
    2.获取redis 数据
    3.对redis的数据进行转换
    4. 合并前初始化记录 ( 保留redis的数据, 初始化一个选中的id列表)
    5. 合并
    6. 将合并的数据保存到redis中
    """

    # 1.获取cookie数据
    cookie_str = request.COOKIES.get('cart')
    if cookie_str is not None:
        #说明有数据
        cookie_cart =  pickle.loads(base64.b64decode(cookie_str))
        # {1: {count:10,selected:True}, 3:{count:30,selected:False}}

        # 2.获取redis 数据
        redis_conn = get_redis_connection('cart')

        # user = request.user
        #hash
        redis_id_counts = redis_conn.hgetall('cart_%s'%user.id)
        # {b'2':b'20',b'3':b'100'}

        # 3.对redis的数据进行转换
        redis_cart = {}
        for sku_id,count in redis_id_counts.items():
            redis_cart[int(sku_id)]=int(count)

        # redis_cart
        #{2:20,3:100}

        # 4. 合并前初始化记录 ( 保留redis的数据, 初始化一个选中的id列表)
        cookie_selected_ids = []

        # 5. 合并
        # {1: {count:10,selected:True}, 3:{count:30,selected:False}}

        for sku_id,count_selected_dict in cookie_cart.items():
            # if sku_id in redis_cart:
            #     redis_cart[sku_id]=count_selected_dict['count']
            # else:

            redis_cart[sku_id]=count_selected_dict['count']

            # 选中的状态
            if count_selected_dict['selected']:
                cookie_selected_ids.append(sku_id)

        # 6. 将合并的数据保存到redis中
        # 更新 hash
        # redis_cart = {sku_id:count,sku_id:count}
        redis_conn.hmset('cart_%s'%user.id,redis_cart)


        # 保存选中的id
        # cookie_selected_ids = [1,2,3,4]
        redis_conn.sadd('cart_selected_%s'%user.id,*cookie_selected_ids)

        # 7. cookie数据删除
        response.delete_cookie('cart')

        # 相应对象我们只是使用一下,一定要返回
        return response

    return response
'''