from django_redis import get_redis_connection
import random

Conn = get_redis_connection('default')


def get_identify_and_set_cache(key: str, digit: int, time: int) -> str:
    """
    取得隨機數字，並將該數字以{key: 隨機數字}暫存在redis裡(保持time秒)
    :param key: 要寫入redis的key
    :param digit: 產生幾個隨機數字
    :param time: 該鍵值資料要存放在redis多久
    :return: 隨機數字
    """
    number = ''.join([str(random.randint(0, 9)) for _ in range(digit)])
    Conn.set(key, number, ex=time)
    return number
