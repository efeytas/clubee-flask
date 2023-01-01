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

    def test_register_user(self):
        # create a test client
        client = application.test_client()
        # send a request to the registration endpoint
        response = client.post('/api/register', data=json.dumps({
        "full_name": "John Doe",
        "email": "john.doe@gmail.com",
        "amazon_id": "12345678",
        "studentnumber": "123456"
        }), content_type='application/json',headers={
'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b'"Registered"\n')


    def test_register_already_existing_user(self):
            # create a test client
        client = application.test_client()
            # send a request to the registration endpoint
        response = client.post('/api/register', data=json.dumps({
                "full_name": "John Doe",
                "email": "john.doe@gmail.com",
                "amazon_id": "12345678",
                "studentnumber": "123456"
            }), content_type='application/json',headers={
'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
            # check the response status code
        self.assertEqual(response.status_code, 200)
            # check the response data
        self.assertEqual(response.data, b'"User already exists"\n')

    def test_join_event(self):
        # create a test client
        client = application.test_client()
        # send a request to the join event endpoint
        response = client.post('/api/event/join', data=json.dumps({
        "eventid": 1,
        "studentnumber": "123456"
        }), content_type='application/json', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b"Joined")

    def test_join_already_joined_event(self):
        # create a test client
        client = application.test_client()
        # send a request to the join event endpoint
        response = client.post('/api/event/join', data=json.dumps({
            "eventid": 1,
            "studentnumber": "123456"
        }), content_type='application/json', headers={
            'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b"Already joined")

    def test_get_profile(self):
            # create a test client
            client = application.test_client()
            # send a request to the profile endpoint
            response = client.get('/api/profile/150180086', headers={
            'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
            # check the response status code
            self.assertEqual(response.status_code, 200)
            # check the response data
            self.assertEqual(response.data, b'[[6,"Efe Yigit Tas","tase18@itu.edu.tr",null,"150180086"]]\n') 


    def test_get_chapter(self):
            # create a test client
            client = application.test_client()
            # send a request to the chapter endpoint
            response = client.get('/api/chapter/2', headers={
            'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
            # check the response status code
            self.assertEqual(response.status_code, 200)
            # check the response data
            self.assertEqual(response.data, b'[[2,"DSC ITU is a non-profit developer group to learn, share, connect and delevop tech skills. Join us!","ITU DSC ",1,7]]')

    def test_get_all_events(self):
        # create a test client
        client = application.test_client()
        # send a request to the all events endpoint
        response = client.get('/api/events/all', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b'[[1,"ITU DSC First Meetup","Welcome to our first meetup, we will be discussing about DSC and its vision and future events.","2022-03-01 15:00:00",1,1,1,1],[2,"ITU DSC Workshop: Introduction to Web Development","Join us in this workshop to learn the basics of web development and build your first website.","2022-03-15 14:00:00",2,2,1,1],[3,"ITU DSC Workshop: Introduction to Machine Learning","Join us in this workshop to learn the basics of machine learning and build your first machine learning model.","2022-03-17 14:00:00",2,2,1,1],[4,"ITU DSC Hackathon","Join us in this hackathon to solve real-world problems and showcase your skills.","2022-03-20 10:00:00",2,2,1,1]]')


    def test_get_event(self):
        # create a test client
        client = application.test_client()
        # send a request to the all events endpoint
        response = client.get('/api/events/1', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b'[[1,"DSC ITU is a non-profit developer group to learn, share, connect and delevop tech skills. Join us!","ITU DSC ",1,7]]')

    def test_get_highlighted_events(self):
        # create a test client
        client = application.test_client()
        # send a request to the all events endpoint
        response = client.get('/api/events/highlighted', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b'[[1,"DSC ITU is a non-profit developer group to learn, share, connect and delevop tech skills. Join us!","ITU DSC ",1,7]]')

    def test_get_members_active_chapters(self):
        client = application.test_client()
        # send a request to the all events endpoint
        
        response = client.get('/api/activechapters/150180086', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b'[["ITU ACM Student Chapter"],["ITU AI Student Club"],["ITU DSC "]]\n')

    def test_get_events_participated(self):
        client = application.test_client()
        # send a request to the all events endpoint
        
        response = client.get('/api/event/participated/150180086', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b'[[1,"algoComp\'23","algoComp\'23 is an algo[484 chars]]]\n]')
    #HTML Tests Admin Page

    def test_get_event_applied(self):
        client = application.test_client()
        # send a request to the all events endpoint
        
        response = client.get('/api/event/applied/150180086', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        # check the response status code
        self.assertEqual(response.status_code, 200)
        # check the response data
        self.assertEqual(response.data, b'[[1,"algoComp\'23","algoComp\'23 is an algo[484 chars]]]\n')
    #HTML Tests Admin Page

    
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
    

class IntegrationTest(unittest.TestCase):
    """
    signup->view profile->join to event-> event applied->view events participated->active chapter
    
    """
    def setUp(self):
        self.app = application.test_client()#client
        self.app.testing = True

    def IntegrationTest(self):
         # send a request to the profile endpoint
        self.app.get('/api/profile/150180086', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        self.app.post('/api/event/join', data=json.dumps({
        "eventid": 1,
        "studentnumber": "123456"
        }), content_type='application/json', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        response=self.app.get('/api/event/applied/150180086', headers={
        'Content-Type': 'application/json', 'auth-key': "0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30"
})
        self.assertEqual(response.status_code, 200)
        



if __name__ == '__main__':
    unittest.main()
