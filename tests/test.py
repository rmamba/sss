from StringIO import StringIO
from sss3.sss3 import SSS3

import unittest
import sys
import json
import os.path

class testConfigCommandWithNoConfigFile(unittest.TestCase):
  def setUp(self):
    self.held, sys.stdout = sys.stdout, StringIO()

  def test_no_arguments(self):
    SSS3(['sss3.py'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration')

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

  # def test_set_AWS_wrong_credentials(self):
  #   SSS3(['sss3.py', 'config', 'AWS', 'notAccess', 'notKey'])
  #   self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')
  #
  # def test_set_AWS_correct_credentials(self):
  #   SSS3(['sss3.py', 'config', 'AWS', 'rightAccess', 'rightKey'])
  #   self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

class testWithConfigFileRestrectedAccess(unittest.TestCase):
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

    data = {"GUID": self.test_data['names']['existing'], "Secret_Access_Key": self.test_data['AWS']['restrected']['AccessKeyID'], "Access_Key_ID": self.test_data['AWS']['restrected']['SecretAccessKey']}
    with open(self.FOLDER_NAME, 'w') as outfile:
      json.dump(data, outfile)

  def test_no_arguments(self):
    SSS3(['sss3.py'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration')

  def test_config_no_parameters(self):
    SSS3(['sss3.py', 'config'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 config <argument> <argument> <argument>\n\nArguments:\n\tAWS\tPrints AWS credentials. Or sets credentials if new are provided.\n\tGUID\tPrint name of this repository.')

  def test_config_print_GUID(self):
    SSS3(['sss3.py', 'config', 'GUID'])
    self.assertEqual(sys.stdout.getvalue(), 'GUID: sss3-test\n')

  def test_config_set_GUID(self):
    SSS3(['sss3.py', 'config', 'GUID', 'newGUID'])
    self.assertEqual(sys.stdout.getvalue(), 'GUID is read only!!!\n')

  def test_config_set_GUID2(self):
    SSS3(['sss3.py', 'config', 'GUID', 'newGUID', 'dummyGUID'])
    self.assertEqual(sys.stdout.getvalue(), 'GUID is read only!!!\n')

  def test_config_print_AWS(self):
    SSS3(['sss3.py', 'config', 'AWS'])
    self.assertEqual(sys.stdout.getvalue(), 'AccessKeyID: \t{0}\nSecretAccessKey: \t{1}'.format(self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']))

  def test_config_set_AWS_not_enough_parameters(self):
    SSS3(['sss3.py', 'config', 'AWS', 'notEnough' ])
    self.assertEqual(sys.stdout.getvalue(), 'You need to specify both AccessKeyID and SecretAccessKey to change them!!!\n')

  # def test_config_set_AWS_wrong_credentials(self):
  #   SSS3(['sss3.py', 'config', 'AWS', 'notAccess', 'notKey'])
  #   self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')
  #
  # def test_config_set_AWS_correct_credentials(self):
  #   SSS3(['sss3.py', 'config', 'AWS', 'rightAccess', 'rightKey'])
  #   self.assertEqual(sys.stdout.getvalue(), 'This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.\n')

if __name__ == '__main__':
    unittest.main()
