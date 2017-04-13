try:
  from StringIO import StringIO
except ImportError:
  from io import StringIO
from sss3.sss3 import SSS3

import unittest
import sys
import os
import json
import shutil
import time


class TestAddNoConfig(unittest.TestCase):
    test_data = None
    TEST_FILE = 'testdata.json'
    FOLDER_NAME = '.sss3'
    CONFIG_FILE = './{0}/config.json'.format(FOLDER_NAME)
    CONTENT_FILE = './{0}/content.json'.format(FOLDER_NAME)

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        if os.path.isfile(self.CONFIG_FILE):
            os.remove(self.CONFIG_FILE)
        with open(self.TEST_FILE) as json_data:
            self.test_data = json.load(json_data)

        if not os.path.isdir(self.FOLDER_NAME):
            os.makedirs(self.FOLDER_NAME)

        with open(self.CONTENT_FILE, 'w') as f:
            f.write('{}')

        with open('test', 'w') as f:
            f.write('{}'.format(time.time()))

    def test_01_no_arguments(self):
        SSS3(['sss3.py', 'add'])
        self.assertEqual(sys.stdout.getvalue(), 'No file specified! Specify which file to add to the repository or use help command to find out more.\n')
        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        self.assertEqual(data, '{}')

    def test_02_no_config_error(self):
        SSS3(['sss3.py', 'add', 'test'])
        self.assertEqual(sys.stdout.getvalue(), 'Configuration setup missing, please run init command first.\n')
        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        self.assertEqual(data, '{}')


class TestAddWithConfig(unittest.TestCase):
    test_data = None
    TEST_FILE = 'testdata.json'
    FOLDER_NAME = '.sss3'
    CONFIG_FILE = './{0}/config.json'.format(FOLDER_NAME)
    CONTENT_FILE = './{0}/content.json'.format(FOLDER_NAME)

    @staticmethod
    def __createFile(name):
        with open(name, 'w') as f:
            f.write('{}'.format(int(time.time())))

    def __clean(self):
        if os.path.isdir(self.FOLDER_NAME):
            shutil.rmtree(self.FOLDER_NAME)
        if os.path.isfile('test'):
            os.remove('test')
        if os.path.isfile('test2'):
            os.remove('test2')

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        with open(self.TEST_FILE) as json_data:
            self.test_data = json.load(json_data)

        self.__clean()
        os.makedirs(self.FOLDER_NAME)
        with open(self.CONTENT_FILE, 'w') as f:
            f.write('{}')

        self.__createFile('test')

        data = {"GUID": self.test_data['names']['existing'],
                "Secret_Access_Key": self.test_data['AWS']['restrected']['SecretAccessKey'],
                "Access_Key_ID": self.test_data['AWS']['restrected']['AccessKeyID']}
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(data, f)

    def test_01_none_existing_file(self):
        SSS3(['sss3.py', 'add', 'test2'])
        self.assertEqual(sys.stdout.getvalue(), 'Error: File: test2 missing!\n')

        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        self.assertEqual(json_data.keys(), [])

    def test_02_add_file(self):
        SSS3(['sss3.py', 'add', 'test'])
        # self.assertEqual(sys.stdout.getvalue(), 'File(s) added successfully.\n')

        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        self.assertEqual(json_data.keys(), [u'test', u'.sss3'])
        self.assertEqual(json_data[u'test'][u'size'], 10)
        self.assertEqual(json_data[u'.sss3'].keys(), [u'children'])
        self.assertEqual(json_data[u'.sss3'][u'children'].keys(), [u'content.json'])

    def test_03_add_two_files_error(self):
        SSS3(['sss3.py', 'add', 'test', 'test2'])
        self.assertEqual(sys.stdout.getvalue(), 'Error: File: test2 missing!\n')

        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        self.assertEqual(json_data.keys(), [u'test', u'.sss3'])
        self.assertEqual(json_data[u'test'][u'size'], 10)
        self.assertEqual(json_data[u'.sss3'].keys(), [u'children'])
        self.assertEqual(json_data[u'.sss3'][u'children'].keys(), [u'content.json'])

    def test_04_add_two_files(self):
        self.__createFile('test2')
        SSS3(['sss3.py', 'add', 'test', 'test2'])
        # self.assertEqual(sys.stdout.getvalue(), 'File(s) added successfully.\n')

        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        self.assertEqual(json_data.keys(), [u'test', u'test2', u'.sss3'])
        self.assertEqual(json_data[u'test'].keys(), [u'last_modified_timestamp', u'created_timestamp', u'size', u'type', u'crc'])
        self.assertEqual(json_data[u'test'][u'size'], 10)
        self.assertEqual(json_data[u'test2'][u'size'], 10)
        self.assertEqual(json_data[u'.sss3'].keys(), [u'children'])
        self.assertEqual(json_data[u'.sss3'][u'children'].keys(), [u'content.json'])

    def test_05_wildcard(self):
        SSS3(['sss3.py', 'add', 'test*'])

        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        self.assertEqual(json_data.keys(), [u'test', u'test2', u'.sss3'])
        self.assertEqual(json_data[u'test'][u'size'], 10)
        self.assertEqual(json_data[u'test2'][u'size'], 10)
        self.assertEqual(json_data[u'.sss3'].keys(), [u'children'])
        self.assertEqual(json_data[u'.sss3'][u'children'].keys(), [u'content.json'])

    def test_06_all_files(self):
        SSS3(['sss3.py', 'add', '.'])
        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        self.assertEqual(json_data.keys(), [u'__init__.pyc', u'test-help.py', u'test-remove.py', u'.sss3', u'test-config.py', u'testdata.json', u'__init__.py', u'.coverage', u'test-add.py', u'test-workflow.py', u'test-init.py', u'test', u'test-clone.py', u'__pycache__'])
        self.assertEqual(json_data[u'.sss3'].keys(), [u'children'])
        self.assertEqual(json_data[u'.sss3'][u'children'].keys(), [u'content.json'])

    def test_07_existing_file(self):
        SSS3(['sss3.py', 'add', 'test'])
        SSS3(['sss3.py', 'add', 'test'])
        self.assertEqual(sys.stdout.getvalue(), 'File already in repository.\n')

    def test_07_update_file(self):
        SSS3(['sss3.py', 'add', 'test'])
        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        crc =  json_data[u'test'][u'crc']
        self.__createFile('test')
        SSS3(['sss3.py', 'add', 'test'])
        data = None
        with open(self.CONTENT_FILE, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        self.assertEqual(sys.stdout.getvalue(), 'File updated in repository.\n')
        self.assertNotEqual(json_data[u'test'][u'crc'], crc)

    # def test_99_clean(self):
    #     self.__clean()
    #     self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
