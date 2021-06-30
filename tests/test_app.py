import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../','app_main'))

from app_main.app import app, main
import unittest


class FlaskTestCase(unittest.TestCase):
    def test_trial(self):

        tester = app.test_client(self)
        response = tester.get('/testpage',content_type='application/json')
        print(response.json["description"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["description"], 'My First Heading')
    
    def test_dataflow(self):
        
        tester = app.test_client(self)
        response = tester.post('/testpage', data= dict( caption_image = open(os.path.join(os.getcwd(),'app_main','caption_images','doggy269.jpg'),'rb')) )
        print("Hello")
        print(response.json)
        expected_strings = ["dog","beach"]
        self.assertTrue(all(x in str(response.json["description"]) for x in expected_strings ))

    