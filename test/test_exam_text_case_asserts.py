"""
Tests assertmethods in examiner.exam_test_case.py.
"""
import sys
import os
import unittest
from unittest.runner import _WritelnDecorator
from unittest import SkipTest

proj_path = os.path.dirname(os.path.realpath(__file__ + "/../"))
path = proj_path + "/examiner"
if path not in sys.path:
    sys.path.insert(0, path)

import exceptions as exce
from exam_test_case import ExamTestCase

class Test_ExamTestCase(unittest.TestCase):

    def test_assert_not_in_pass(self):
        """
        Test that assertNotIn works when passing
        """
        class Test1AssertNotIn(ExamTestCase):
            def test_a_foo(self_):
                self_.tags = ['test', 'assert']
                self_.assertNotIn('correct', ['incorrect'])

        test = Test1AssertNotIn('test_a_foo')
        test.test_a_foo()

        self.assertEqual(test.correct_answer, "'correct'")
        self.assertEqual(test.student_answer, "['incorrect']")
        self.assertEqual(test.tags, ['test', 'assert'])
        # check that method was decorated for tags
        self.assertEqual(getattr(test.assertNotIn, "__wrapped__").__name__, "assertNotIn")



    def test_assert_not_in_fail(self):
        """
        Test that assertNotIn works when failing
        """
        class Test1AssertNotIn(ExamTestCase):
            def test_a_foo(self_):
                self_.assertNotIn('correct', ['correct', 'incorrect'])

        test = Test1AssertNotIn('test_a_foo')
        with self.assertRaises(AssertionError):
            test.test_a_foo()

        self.assertEqual(test.correct_answer, "'correct'")
        self.assertEqual(test.student_answer, "['correct', 'incorrect']")
        self.assertEqual(test.tags, [])


if __name__ == '__main__':
    # runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(verbosity=2)
