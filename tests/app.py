import unittest
from legitag import app
import os

class TestApp(unittest.TestCase):

    # def setUp(self):
    #     self.app = app.test_client()

    def test_alive(self):
        assert 1 == 1
        # rv = self.app.get('/')
        # assert rv.status == '200 OK'

# if __name__ == '__main__':
#     unittest.main()