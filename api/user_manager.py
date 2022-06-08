from api.base import Base
from loguru import logger


class UserManager(Base):

    # 初始化接口路径
    def __init__(self):
        self.add_user_url = self.get_url("/admin/admin/create")
        self.edit_user_url = self.get_url("/admin/admin/update")
        self.search_user_url = self.get_url("/admin/admin/list?page=1&limit=20&sort=add_time&order=desc")
        self.delete_user_url = self.get_url("/admin/admin/delete")

    # 新增用户
    def add_user(self, username, password, **kwargs):
        """
        请求的是添加管理员的接口
        :return: json数据
        """
        user_data = {"username": username, "password": password}
        if kwargs:
            logger.info("添加管理员可选参数{}", **kwargs)
            user_data.update(**kwargs)
        return self.post(self.add_user_url, user_data)

    # 查询用户
    def search_user(self):
        """
        请求的查询管理员的接口
        :return: json数据
        """
        return self.get(self.search_user_url)

    # 修改用户
    def edit_user(self, id, username, password, **kwargs):
        """
        请求的修改管理员的接口
        :return: json数据
        """
        user_data = {"id": id, "username": username, "password": password}
        if kwargs:
            user_data.update(**kwargs)
        return self.post(self.edit_user_url, user_data)

    # 删除用户
    def delete_user(self, id, username, **kwargs):
        """
        请求的删除管理员的接口
        :return: json数据
        """
        user_data = {"id": id, "username": username}
        if kwargs:
            user_data.update(**kwargs)
        return self.post(self.delete_user_url, user_data)

