import requests
import unittest
"""
pip install requests
"""

class AccountTests(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:8000/api/account/'

    def test_register(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = requests.post(self.base_url + 'register/', json=data)
        print(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], '注册成功')

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123123'
        }
        response = requests.post(self.base_url + 'login/', json=data)
        print(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

if __name__ == '__main__':
    unittest.main()