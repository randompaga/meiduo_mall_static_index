import base64
import pickle

from django_redis import get_redis_connection

def merge_cart_cookie_to_redis(request,user,response):
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
