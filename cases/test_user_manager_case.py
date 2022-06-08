# 用户管理中的测试用例
import unittest
from api.user_manager import UserManager
from data.user_manager_data import UserManagerData


class TestUserManager(unittest.TestCase):
    user_id = 0

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = UserManager()
        # cls.user.login()
        cls.user_id = TestUserManager.user_id
        cls.username = UserManagerData.add_user_data.get("username")
        cls.password = UserManagerData.add_user_data.get("password")
        cls.new_username = UserManagerData.add_user_data.get("new_username")
        # cls.username = "tester01"
        # cls.password = "123456"
        # cls.new_username = "testery01"

    # 添加管理员：只输入用户名和密码的情况
    def test01_add_user(self):
        # 1.初始化添加管理员的测试数据
        # self.user_id = None
        # 2.调用添加管理员接口
        actual_result = self.user.add_user(self.username, self.password)
        data = actual_result.get("data")
        if data:
            TestUserManager.user_id = data.get("id")
        # 3.运行断言
        self.assertEqual(UserManagerData.add_user_data.get("errno"), actual_result["errno"])
        self.assertEqual(self.username, actual_result.get("data").get("username"))

    # 编辑用户：修改的是用户名
    def test02_edit_username(self):
        # pass
        # 1.定义测试数据

        # 2.调用修改管理员接口
        actual_result = self.user.edit_user(self.user_id, self.new_username, password=123456)
        # 3.断言
        self.assertEqual(UserManagerData.add_user_data.get("errno"), actual_result["errno"])
        self.assertEqual(self.new_username, actual_result.get("data").get("username"))

    # 查询用户列表
    def test03_search_user(self):
        # 调用查询管理员接口
        actual_result = self.user.search_user()

        # 断言
        self.assertEqual(UserManagerData.add_user_data.get("errno"), actual_result["errno"])
        self.assertEqual(self.new_username, actual_result.get('data').get('list')[0].get("username"))

    # 删除用户
    def test04_delete_user(self):
        # 定义删除数据

        # 调用删除管理员接口
        actual_result = self.user.delete_user(self.user_id, self.username)

        # 断言
        self.assertEqual(UserManagerData.add_user_data.get("errno"), actual_result["errno"])
        self.assertEqual("成功", actual_result.get("errmsg"))


if __name__ == '__main__':
    unittest.main()
