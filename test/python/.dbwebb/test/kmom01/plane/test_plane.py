#!/usr/bin/env python3
"""
Contains testcases for the individual examination.
"""
import unittest
from unittest.mock import patch
from importlib import util
from io import StringIO
import os
import sys
from unittest import TextTestRunner
from exam_test_case import ExamTestCase
from exam_test_result import ExamTestResult
from helper_functions import import_module


# Calculates the path to the import file - Given it has the same folder structure as the me-folder
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_DIR_LIST = FILE_DIR.split("/")
FILE_DIR_LEN = len(FILE_DIR_LIST) - 1
FOLDERS_TO_ROOT = FILE_DIR_LEN - FILE_DIR_LIST.index('python')
COURSE_ROOT = '../' * FOLDERS_TO_ROOT
KMOM_AND_ASSIGNENT = "/".join(FILE_DIR_LIST[-(FOLDERS_TO_ROOT - 2):])
REPO_PATH = f"{FILE_DIR}/{COURSE_ROOT}me/{KMOM_AND_ASSIGNENT}"


if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

# Path to file and basename of the file to import
# plane = import_module(REPO_PATH, "plane") # Has inputs, use in check_print 



class Test1Plane(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.

    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """

    @classmethod
    def setUpClass(cls):
        # Otherwise the .txt files will not be found
        os.chdir(REPO_PATH)

    def check_print_contain(self, inp, correct):
        """
        One function for testing print input functions
        """
        with patch('builtins.input', side_effect=inp):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                plane = import_module(REPO_PATH, "plane")
                str_data = fake_out.getvalue()
                self.assertIn(correct, str_data)

    def test_a_temperature(self):
        """
        Testar temeraturen
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.tags = ["temp"]
        self.norepr = True
        self._argument = ["100", "100", "100"]
        self.check_print_contain(self._argument, "212.0")
    
    def test_b_speed(self):
        """
        Testar hastigheten
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.tags = ["speed"]
        self.norepr = True
        self._argument = ["100", "100", "100"]
        self.check_print_contain(self._argument, "62.14")


    def test_c_height(self):
        """
        Testar hastigheten
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.tags = ["height"]
        self.norepr = True
        self._argument = ["100", "100", "100"]
        self.check_print_contain(self._argument, "328.08")

if __name__ == '__main__':
    runner = TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(testRunner=runner, exit=False)
