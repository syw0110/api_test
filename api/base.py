"""
主要用于所有接口的公共功能
1.处理url
2.重新封装get方法，post方法
3.处理headers
4.登录
"""
from setting import BASE_URL,LOGIN_INFO
import requests
from loguru import logger
from cacheout import Cache

# 创建了cache对象
cache = Cache()


class Base():

    # 实现url的拼接
    def get_url(self, path, params=None):
        # 判断是否有参数，没有就返回基本路径加上path
        # path: 接口路径：/admin/auth/login
        # params: q=iphone
        if params:
            full_url = BASE_URL + path + params
            return full_url
        return BASE_URL + path

    # get方法
    def get(self, url):
        result = None
        response = requests.get(url, headers=self.get_headers())
        try:
            result = response.json()  # 获取响应体中的json数据
            logger.success(f"请求URL：{url}，返回结果：{result}")
            return result
        except Exception as e:
            logger.error(f"请求post方法异常，返回数据：{result}")

    # post方法
    def post(self, url, data):
        """
        在原来的基础上新增日志，返回json格式
        :return: json
        """
        result = None
        response = requests.post(url, json=data, headers=self.get_headers())
        try:
            result = response.json()  # 获取响应体中的json数据
            logger.success(f"请求URL：{url}，请求参数：{data}，返回结果：{result}")
            return result
        except Exception as e:
            logger.error(f"请求post方法异常，返回数据：{result}")

    # headers
    def get_headers(self):
        """
        返回的是字典格式的请求头,包括了Content-Type,X-Litemall-Admin-Token
        :return:
        """
        headers = {"Content-Type":"application/json"}
        token = cache.get("token") # 从缓存中获取token
        if token:
            headers.update({"X-Litemall-Admin-Token":token})
            return headers
        return headers

    # 登录
    def login(self):
        """
        通过调用登录接口获取token，保存，其他接口使用时，直接从缓存中取出token
        如果没有取到，再调用登录，再将token放到缓存中
        :return: token
        """
        login_path = "/admin/auth/login"
        login_url = self.get_url(login_path)   # 拼接登录的接口地址
        result = self.post(login_url,LOGIN_INFO)  # 请求登录接口，返回json
        try:
            if result.get("errno") == 0:
                logger.info("请求登录接口成功")
                token = result.get("data").get("token")
                cache.set("token", token)
            else:
                logger.error(f"登录失败：{result}")
                return None
        except Exception as e:
            logger.error(f"报错信息：{e}")
            logger.error(f"请求登录接口返回异常,异常数据:{result}")


# if __name__ == '__main__':
#     base = Base()
    # print(base.get_url('/admin/auth/login'))
    # print(base.get_url('/admin/admin/list','page=1&limit=20&sort=add_time&order=desc'))
    # login_url = base.get_url("/admin/auth/login")
    # print(base.post(login_url, LOGIN_INFO))
    # print(base.get(login_url))
    # base.login()
    # print(cache.get("token"))