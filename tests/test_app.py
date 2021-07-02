import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../','app_main'))

from app_main.app import app, main
import unittest
import pytest

class FlaskTestCase(unittest.TestCase):
    def test_trial(self):

        tester = app.test_client(self)
        response = tester.get('/testpage',content_type='application//json')
        print(response.json["description"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["description"], 'My First Heading')
    
    

    def test_dataflow(self):
        #this works fine, now we have to work on error handling
        input_value = [
            [['app_main', 'caption_images', 'doggy269.jpg'], ['dog', 'beach']],
            [['app_main', 'caption_images', 'playing.jpeg'], ['playing', 'soccer']],
            [['app_main', 'caption_images', 'laptop.png'], ['man', 'bench']],
            ]#test conditions for different image formats
        #expected=[['dog','beach']]
        for i,j in input_value:
            tester = app.test_client(self)
            response = tester.post('/testpage', data= dict( caption_image = open(os.path.join(os.getcwd(),i[0],i[1],i[2]),'rb')) )
            print(response.json)
            expected_strings = j
            self.assertTrue(all(x in str(response.json["description"]) for x in expected_strings ))
        #below code is for checking for error when file format is incorrect
        input_value = [
            [['app_main', 'caption_images','shh.txt'], ["Non-Existent or Invalid File Upload"]]
        ]
        for i,j in input_value:
            tester = app.test_client(self)
            response = tester.post('/testpage', data= dict( caption_image = open(os.path.join(os.getcwd(),i[0],i[1],i[2]),'rb')) )
            print(response.json)
            expected_strings = j
            pytest.raises(TypeError)
        #test if file is non-existant
        input_value = [
            [['app_main', 'caption_images',''], ["Non-Existent or Invalid File Upload"]]
        ]
        for i,j in input_value:
            tester = app.test_client(self)
            pytest.raises(FileNotFoundError)


    
