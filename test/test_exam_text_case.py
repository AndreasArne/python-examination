"""
Use this to test our new and added functionality.
"""
import sys
import unittest
from unittest.runner import _WritelnDecorator
from app.exam_textcase import ExamTestCase



class Test_ExamTestCase(unittest.TestCase):

    def test_set_test_name_and_assignment(self):
        """
        Tests that set_test_name_and_assignment extracts test name and assignment
        correct.
        """
        class TestAssignment1(ExamTestCase):
            def test_a_foo(self):
                pass
        
        test = TestAssignment1('test_a_foo')
        # test._set_test_name_and_assignment()
        self.assertEqual(test.assignment, "Assignment1")
        self.assertEqual(test.test_name, "foo")



    def test_set_test_name_and_assignment_rasie_exception_missing_identifier(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when test function
        miss identifier after letter.
        """
        class TestAssignment1(ExamTestCase):
            def test_a(self):
                pass

        with self.assertRaises(ValueError) as cxt:
            test = TestAssignment1('test_a')



    def test_set_test_name_and_assignment_rasie_exception_missing_lettert(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when test function
        miss letter.
        """
        class TestAssignment1(ExamTestCase):
            def test_foo(self):
                pass

        with self.assertRaises(ValueError) as cxt:
            test = TestAssignment1('test_foo')



    def test_set_test_name_and_assignment_rasie_exception_missing_assignment(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when class name
        miss "Assignment".
        """
        class Testassignment1(ExamTestCase):
            def test_a_foo(self):
                pass

        with self.assertRaises(ValueError) as cxt:
            test = Testassignment1('test_a_foo')



    def test_set_test_name_and_assignment_rasie_exception_missing_number(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when class name
        number is missing.
        """
        class TestAssignment(ExamTestCase):
            def test_a_foo(self):
                pass

        with self.assertRaises(ValueError) as cxt:
            test = TestAssignment('test_a_foo')



if __name__ == '__main__':
    # runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(verbosity=2)
