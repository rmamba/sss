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


class TestCloneCommandWithRestrectedAccess(unittest.TestCase):
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

    if os.path.isdir(self.FOLDER_NAME):
      # Remove folder if it exist
      shutil.rmtree(self.FOLDER_NAME)
    if os.path.isdir('test'):
      os.remove('test')

  def test_01_no_parameters(self):
    SSS3(['sss3.py', 'clone'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_02_one_parameter(self):
    SSS3(['sss3.py', 'clone', 'sss3-push-test'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_03_two_parameters(self):
    SSS3(['sss3.py', 'clone', 'sss3-push-test', 'random'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_04_clone_no_access(self):
    SSS3(['sss3.py', 'clone', 'sss3-push-test', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'File downloaded: .sss3/content.json complete\nFile downloaded: test complete\n')
    self.assertTrue(os.path.isfile('test'))
    self.assertTrue(os.path.isfile(self.CONTENT_FILE))
    self.assertTrue(os.path.isfile(self.CONFIG_FILE))

  def test_05_clone_full_access(self):
    SSS3(['sss3.py', 'clone', 'sss3-push-test', self.test_data['AWS']['unrestrected']['AccessKeyID'], self.test_data['AWS']['unrestrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'File downloaded: .sss3/content.json complete\nFile downloaded: test complete\n')
    self.assertTrue(os.path.isfile('test'))
    self.assertTrue(os.path.isfile(self.CONTENT_FILE))
    self.assertTrue(os.path.isfile(self.CONFIG_FILE))

  def test_99_clean(self):
    if os.path.isdir(self.FOLDER_NAME):
      shutil.rmtree(self.FOLDER_NAME)
    if os.path.isdir('test'):
      os.remove('test')
    self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
