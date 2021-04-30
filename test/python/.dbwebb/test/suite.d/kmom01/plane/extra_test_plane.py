#!/usr/bin/env python3
"""
Example for an extra assignment, has no other function.
"""
import unittest
import os
import sys
from unittest import TextTestRunner
from examiner.exam_test_case import ExamTestCase
from examiner.exam_test_result import ExamTestResult
from examiner.helper_functions import find_path_to_assignment


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = find_path_to_assignment(FILE_DIR)


if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

# Path to file and basename of the file to import
# plane = import_module(REPO_PATH, "plane")



class Test2PlaneExtra(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.

    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """

    @classmethod
    def setUpClass(cls):
        # Otherwise the .txt files will not be found
        os.chdir(REPO_PATH)

    def test_a_no_extra_assignments(self):
        """
        Ingen extra uppgift.
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.tags = ["speed", "temp", "height"]
        self.assertTrue(False)

if __name__ == '__main__':
    runner = TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(testRunner=runner, exit=False)
