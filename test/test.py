from myproject import app
import unittest


class WatchlistTestCase(unittest.TestCase):

    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING=True,
        )
        # # 创建数据库和表
        # db.create_all()
        # # 创建测试数据，一个用户，一个电影条目
        # user = User(name='Test', username='test')
        # user.set_password('123')
        # movie = Movie(title='Test Movie Title', year='2019')
        # # 使用 add_all() 方法一次添加多个模型类实例，传入列表
        # db.session.add_all([user, movie])
        # db.session.commit()

        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    # def tearDown(self):
    #     db.session.remove()  # 清除数据库会话
    #     db.drop_all()  # 删除数据库表

    # 测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_login_testing(self):
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()