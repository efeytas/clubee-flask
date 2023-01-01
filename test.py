import unittest
from unittest import TestCase
from unittest.mock import patch
import json
import requests

from application import application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = application.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    
    def test_activemember(self):
        response = self.app.get('/admin/activemembers')
        self.assertEqual(response.status_code, 200)
    
    def test_adminprofile(self):
        response = self.app.get('/admin/adminprofile')
        self.assertEqual(response.status_code, 200)
    
    def test_chapterprofile(self):
        response = self.app.get('/admin/chapterprofile')
        self.assertEqual(response.status_code, 200)
    
    def test_events(self):
        response = self.app.get('/admin/events')
        self.assertEqual(response.status_code, 200)

    
    def test_create_event(self):
        response = self.app.get('/admin/events/addevents')
        self.assertEqual(response.status_code, 200)
    
    @patch('requests.post')
    def register_existing(self, mock_post):
        info = {
            "full_name" : "Efe Yigit Tas",
            "email" : "efeytas@gmail.com",
            "amazon_id" : "",
            "studentnumber" : "150180086",
        }
        resp = requests.post('http://clubeeserver.eu-central-1.elasticbeanstalk.com/api/register', data=json.dumps(info))
        mock_post.assert_called_with('http://clubeeserver.eu-central-1.elasticbeanstalk.com/api/register', data=json.dumps(info), headers={'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"})

if __name__ == '__main__':
    unittest.main()
