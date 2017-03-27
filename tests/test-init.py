try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from sss3.sss3 import SSS3

import unittest
import sys
import json
import os.path
import boto3

class TestInitCommandWithRestrectedAccess(unittest.TestCase):
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
    SSS3(['sss3.py', 'init'])
    self.assertEqual(sys.stdout.getvalue(), 'Unable to locate credentials\nusage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_guid(self):
    SSS3(['sss3.py', 'init', 'GUID'])
    self.assertEqual(sys.stdout.getvalue(), 'Unable to locate credentials\nusage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_missing_awskey(self):
    SSS3(['sss3.py', 'init', 'GUID', 'AWSID'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_full_init_wrong_credentials(self):
    SSS3(['sss3.py', 'init', 'GUID', 'AWSID', 'AWSKey'])
    self.assertEqual(sys.stdout.getvalue(), 'An error occurred (InvalidAccessKeyId) when calling the CreateBucket operation: The AWS Access Key Id you provided does not exist in our records.\n')

  def test_full_init_no_guid_rights(self):
    SSS3(['sss3.py', 'init', 'GUID', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'An error occurred (AccessDenied) when calling the CreateBucket operation: Access Denied\n')

  def test_full_init_wrong_domain(self):
    SSS3(['sss3.py', 'init', 'wrong~domain|name', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'You entered invalid domain name!!!\nPlease enter GUID that is also a valid domain name.\n')

  def test_full_init_correct_domain_access_denied(self):
    SSS3(['sss3.py', 'init', 'this-is-correct-domain-name', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'An error occurred (AccessDenied) when calling the CreateBucket operation: Access Denied\n')

  def test_full_init_existing_domain(self):
    SSS3(['sss3.py', 'init', 'sss3-test', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'An error occurred (BucketAlreadyOwnedByYou) when calling the CreateBucket operation: Your previous request to create the named bucket succeeded and you already own it.\n')

  def test_full_init_correct_domain(self):
    bucket_name = 'sss3-init-test'
    session = boto3.Session(aws_access_key_id=self.test_data['AWS']['unrestrected']['AccessKeyID'], aws_secret_access_key=self.test_data['AWS']['unrestrected']['SecretAccessKey'])
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    if bucket in s3.buckets.all():
      bucket.delete()
    SSS3(['sss3.py', 'init', bucket_name, self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'Repository initialised!\n')
    bucket = s3.Bucket(bucket_name)
    if bucket in s3.buckets.all():
      bucket.delete()
    else:
      self.assertTrue(False, 'S3 Bucket was not created!!!')

class TestInitShortCommandWithRestrectedAccess(unittest.TestCase):
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
    SSS3(['sss3.py', 'i'])
    self.assertEqual(sys.stdout.getvalue(), 'Unable to locate credentials\nusage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_guid(self):
    SSS3(['sss3.py', 'i', 'GUID'])
    self.assertEqual(sys.stdout.getvalue(), 'Unable to locate credentials\nusage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_missing_awskey(self):
    SSS3(['sss3.py', 'i', 'GUID', 'AWSID'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

  def test_full_init_wrong_credentials(self):
    SSS3(['sss3.py', 'i', 'GUID', 'AWSID', 'AWSKey'])
    self.assertEqual(sys.stdout.getvalue(), 'An error occurred (InvalidAccessKeyId) when calling the CreateBucket operation: The AWS Access Key Id you provided does not exist in our records.\n')

  def test_full_init_no_guid_rights(self):
    SSS3(['sss3.py', 'i', 'GUID', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'An error occurred (AccessDenied) when calling the CreateBucket operation: Access Denied\n')

  def test_full_init_wrong_domain(self):
    SSS3(['sss3.py', 'i', 'wrong~domain|name', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'You entered invalid domain name!!!\nPlease enter GUID that is also a valid domain name.\n')

  def test_full_init_correct_domain_access_denied(self):
    SSS3(['sss3.py', 'i', 'this-is-correct-domain-name', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'An error occurred (AccessDenied) when calling the CreateBucket operation: Access Denied\n')

  def test_full_init_existing_domain(self):
    SSS3(['sss3.py', 'i', 'sss3-test', self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'An error occurred (BucketAlreadyOwnedByYou) when calling the CreateBucket operation: Your previous request to create the named bucket succeeded and you already own it.\n')

  def test_full_init_correct_domain(self):
    bucket_name = 'sss3-init-test'
    session = boto3.Session(aws_access_key_id=self.test_data['AWS']['unrestrected']['AccessKeyID'], aws_secret_access_key=self.test_data['AWS']['unrestrected']['SecretAccessKey'])
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    if bucket in s3.buckets.all():
      bucket.delete()
    SSS3(['sss3.py', 'i', bucket_name, self.test_data['AWS']['restrected']['AccessKeyID'], self.test_data['AWS']['restrected']['SecretAccessKey']])
    self.assertEqual(sys.stdout.getvalue(), 'Repository initialised!\n')
    bucket = s3.Bucket(bucket_name)
    if bucket in s3.buckets.all():
      bucket.delete()
    else:
      self.assertTrue(False, 'S3 Bucket was not created!!!')

if __name__ == '__main__':
    unittest.main()
