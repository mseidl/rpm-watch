#!/usr/bin/env python
#Martin Seidl
#unit tests for rpm_watch.py

import unittest
import sys
import os
import mock
from StringIO import StringIO
from rpm_watch import *

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class TestRPMWatch(unittest.TestCase):
    '''Test cases for RPMWatch'''
    
    def setUp(self):
        self.rpmw = RPMWatch()
        self.set1 = {1:'a', 2:'b', 3:'c'}
        self.set2 = {2:'b', 3:'c', 4:'d'}
        self.rpm1 = {'name1': [('1','1.1'),0],
                     'name2': [('2.8.2','2.2'),0],
                     'name3': [('1.1.10', '4.99'),0],
                     'name4': [('8.88-git1', '1.0'),0]
                     }
        self.rpm2 = {'name1': [('1','1.10'),0], 
                     'name2': [('2.9.2','2.2'),0],
                     'name3': [('1.1.10', '4.99'),0],
                     'name4': [('7.88-git', '1.0'),0]
                     }
                        

    def tearDown(self):
        pass

    def test_ctor(self):
        '''Test that they are not {} empty, and that they are equal'''
        self.assertTrue(self.rpmw.known_rpms)
        self.assertTrue(self.rpmw.installed_rpms)
        self.assertEqual(self.rpmw.known_rpms, self.rpmw.installed_rpms)
    
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_print_diff_installed(self, mock_stdout):
        print_diff(self.set1, self.set2, 'Installed')
        self.assertEquals(mock_stdout.getvalue(), 'Installed: 1\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_print_diff_removed(self, mock_stdout):
        print_diff(self.set2, self.set1, 'Removed')
        self.assertEquals(mock_stdout.getvalue(), 'Removed: 4\n')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_updated_rpms(self, mock_stdout):
        updated_rpms(self.rpm2, self.rpm1)
        results = mock_stdout.getvalue().split('\n')
        print results
        self.assertEquals(results[0], 'package name4 downgraded')
        self.assertEquals(results[1], 'package name2 upgraded')
        self.assertEquals(results[2], 'package name1 upgraded')


if __name__ == '__main__':
    assert not hasattr(sys.stdout, "getvalue")
    unittest.main(module=__name__, buffer=True, exit=False)
