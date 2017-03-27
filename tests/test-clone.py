try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from sss3.sss3 import SSS3

import unittest
import sys
import os
import json


class TestCloneCommandWithRestrectedAccess(unittest.TestCase):
  test_data = None
  TEST_FILE = 'testdata.json'
  FOLDER_NAME = '.sss3'
  CONFIG_FILE = './{0}/config.json'.format(FOLDER_NAME)

  def setUp(self):
    self.held, sys.stdout = sys.stdout, StringIO()
    if os.path.isfile(self.CONFIG_FILE):
      os.remove(self.CONFIG_FILE)
    with open(self.TEST_FILE) as json_data:
      self.test_data = json.load(json_data)

  def test_no_parameters(self):
    SSS3(['sss3.py', 'clone'])
    self.assertEqual(sys.stdout.getvalue(), 'Unable to locate credentials\nusage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

if __name__ == '__main__':
    unittest.main()
