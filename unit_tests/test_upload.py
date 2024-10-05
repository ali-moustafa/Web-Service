import unittest
from flask import Flask
from werkzeug.datastructures import FileStorage
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from web_app.api.upload import upload_blueprint


class UploadFileTests(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = 'uploads'
        self.app.register_blueprint(upload_blueprint)
        self.client = self.app.test_client()

        if not os.path.exists(self.app.config['UPLOAD_FOLDER']):
            os.makedirs(self.app.config['UPLOAD_FOLDER'])

    def tearDown(self):
        for filename in os.listdir(self.app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
            os.remove(file_path)

    def test_upload_file_success(self):
        """Test successful file upload."""
        file_name = 'test_file.txt'
        data = {
            'file': (FileStorage(stream=open(file_name, 'rb'), filename=file_name), file_name)
        }
        response = self.client.post('/upload', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"File 'test_file.txt' uploaded successfully", response.data)

    def test_upload_no_file(self):
        """Test upload with no file."""
        response = self.client.post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file uploaded!', response.data)

    def test_upload_empty_filename(self):
        """Test upload with an empty filename."""
        data = {
            'file': (FileStorage(stream=open('test_file.txt', 'rb'), filename=''), '')
        }
        response = self.client.post('/upload', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please provide filename!', response.data)


if __name__ == '__main__':
    unittest.main()
