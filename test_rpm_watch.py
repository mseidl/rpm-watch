#!/usr/bin/env python
#Martin Seidl
#unit tests for rpm_watch.py

import unittest
import sys
from rpm_watch import *


class TestRPMWatch(unittest.TestCase):
    '''Test cases for RPMWatch'''
    
    def setUp(self):
        self.rpmw = RPMWatch()
        self.set1 = [1, 2, 3]
        self.set2 = [2, 3, 4]

    def tearDown(self):
        pass

    def test_ctor(self):
        '''Test that they are not {} empty, and that they are equal'''
        self.assertTrue(self.rpmw.known_rpms)
        self.assertTrue(self.rpmw.installed_rpms)
        self.assertEqual(self.rpmw.known_rpms, self.rpmw.installed_rpms)

    def test_print_diff(self):
        print_diff(self.set1, self.set2)
        output = sys.stdout.getvalue().strip()
        self.assertEquals(output, 'Difference: 1')
        sys.stdout.flush()
        print_diff(self.set2, self.set1, 'Foo')
        output2 = sys.stdout.getvalue().strip()
        self.assertEquals(output2, 'Foo: 4')

if __name__ == '__main__':
    assert not hasattr(sys.stdout, "getvalue")
    unittest.main(module=__name__, buffer=True, exit=False)
