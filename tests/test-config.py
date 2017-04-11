try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from sss3.sss3 import SSS3

import unittest
import sys
import json
import os.path
import ctypes

class TestConfigCommandWithNoConfigFile(unittest.TestCase):
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

  def test_01_no_parameters(self):
    SSS3(['sss3.py', 'config'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_02_print_GUID(self):
    SSS3(['sss3.py', 'config', 'GUID'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_03_set_guid(self):
    SSS3(['sss3.py', 'config', 'GUID', 'newGUID'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_04_print_aws(self):
    SSS3(['sss3.py', 'config', 'AWS'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_05_set_aws_not_enough_parameters(self):
    SSS3(['sss3.py', 'config', 'AWS', 'notEnough' ])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_06_set_aws_wrong_credentials(self):
    SSS3(['sss3.py', 'config', 'AWS', 'notAccess', 'notKey'])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

  def test_07_set_aws_correct_credentials(self):
    SSS3(['sss3.py', 'config', 'AWS', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

class TestConfigCommanWithRestrectedAccess(unittest.TestCase):
  test_data = None
  TEST_FILE = 'testdata.json'
  FOLDER_NAME = '.sss3'
  CONFIG_FILE = './{0}/config.json'.format(FOLDER_NAME)

  def setUp(self):
    self.held, sys.stdout = sys.stdout, StringIO()
    if not os.path.isfile(self.TEST_FILE):
      self.skipTest('test data missing...')
    with open(self.TEST_FILE) as json_data:
      self.test_data = json.load(json_data)

    data = {"GUID": self.test_data['names']['existing'], "Secret_Access_Key": self.test_data['AWS']['restrected']['SecretAccessKey'], "Access_Key_ID": self.test_data['AWS']['restrected']['AccessKeyID']}

    if not os.path.isdir(self.FOLDER_NAME):
      if os.name == 'nt':
        os.makedirs(self.FOLDER_NAME)
        ctypes.windll.kernel32.SetFileAttributesW(r'{0}'.format(self.FOLDER_NAME), 0x02)
      else:
        os.makedirs(self.FOLDER_NAME)
      open(self.CONFIG_FILE, 'w').close()
    else:
      if not os.path.isfile(self.CONFIG_FILE):
        open(self.CONFIG_FILE, 'w').close()

    with open(self.CONFIG_FILE, 'w') as outfile:
      json.dump(data, outfile)

  def test_01_no_arguments(self):
    SSS3(['sss3.py'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_02_config_no_parameters(self):
    SSS3(['sss3.py', 'config'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 config <argument> <argument> <argument>\n\nArguments:\n\tAWS\tPrints AWS credentials. Or sets credentials if new are provided.\n\tGUID\tPrint name of this repository.\n')

  def test_03_config_print_guid(self):
    SSS3(['sss3.py', 'config', 'GUID'])
    self.assertEqual(sys.stdout.getvalue(), 'GUID: sss3-test\n')

  def test_04_config_set_guid(self):
    SSS3(['sss3.py', 'config', 'GUID', 'newGUID'])
    self.assertEqual(sys.stdout.getvalue(), 'GUID is read only!!!\n')

  def test_05_config_set_guid2(self):
    SSS3(['sss3.py', 'config', 'GUID', 'newGUID', 'dummyGUID'])
    self.assertEqual(sys.stdout.getvalue(), 'GUID is read only!!!\n')

  def test_06_config_print_aws(self):
    SSS3(['sss3.py', 'config', 'AWS'])
    self.assertEqual(sys.stdout.getvalue(), 'AccessKeyID: \t{0}\nSecretAccessKey: \t{1}\n'.format(self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']))

  def test_07_config_set_aws_not_enough_parameters(self):
    SSS3(['sss3.py', 'config', 'AWS', 'notEnough' ])
    self.assertEqual(sys.stdout.getvalue(), 'You need to specify both AccessKeyID and SecretAccessKey to change them!!!\n')

  def test_08_config_set_aws_wrong_credentials(self):
    SSS3(['sss3.py', 'config', 'AWS', 'notAccess', 'notKey'])
    self.assertEqual(sys.stdout.getvalue(), 'Error accessing S3 bucket!!!\nPlease provide correct credentials that have access to bucket you are using.\n')

  def test_09_config_set_aws_correct_credentials(self):
    SSS3(['sss3.py', 'config', 'AWS', self.test_data['AWS']['unrestrected']['AccessKeyID'], self.test_data['AWS']['unrestrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'New credentials were saved to your configuration file.\n')

if __name__ == '__main__':
    unittest.main()
