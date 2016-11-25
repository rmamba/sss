from StringIO import StringIO
from sss3.sss3 import SSS3

import unittest
import sys

class testSSS3(unittest.TestCase):
  def setUp(self):
    self.held, sys.stdout = sys.stdout, StringIO()

  def test_no_arguments(self):
    SSS3(['sss3.py'])
    self.assertEqual(sys.stdout.getvalue(), '/')

class testConfigCommandWithNoConfigFile(unittest.TestCase):
  def setUp(self):
    self.held, sys.stdout = sys.stdout, StringIO()

  def test_no_parameters(self):
    SSS3(['sss3.py', 'config'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_print_GUID(self):
    SSS3(['sss3.py', 'config', 'GUID'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_set_GUID(self):
    SSS3(['sss3.py', 'config', 'GUID', 'newGUID'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_print_AWS(self):
    SSS3(['sss3.py', 'config', 'AWS'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_set_AWS_not_enough_parameters(self):
    SSS3(['sss3.py', 'config', 'AWS', 'notEnough' ])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_set_AWS_wrong_credentials(self):
    SSS3(['sss3.py', 'config', 'AWS', 'notAccess', 'notKey'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

if __name__ == '__main__':
    unittest.main()
