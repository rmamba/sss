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

  def test_01_init_and_push(self):
    self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
