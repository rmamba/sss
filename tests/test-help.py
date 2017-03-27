try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from sss3.sss3 import SSS3

import unittest
import sys

class TestHelp(unittest.TestCase):
  def setUp(self):
    self.held, sys.stdout = sys.stdout, StringIO()

  def test_no_arguments(self):
    SSS3(['sss3.py'])
    self.assertEqual(sys.stdout.getvalue(), 'usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration\n')

if __name__ == '__main__':
    unittest.main()
