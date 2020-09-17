"""
Use this to test our new and added functionality.
"""
import sys
import unittest
from unittest.runner import _WritelnDecorator
from app.exam_textcase import ExamTestCase



class Test_ExamTestCase(ExamTestCase):

    def test_set_test_name_and_assignment(self):
        """
        Tests that set_test_name_and_assignment extracts test name and assignment
        correct.
        """
        class TestAssignment1(ExamTestCase):
            def test_a_foo(self):
                pass
        
        test = TestAssignment1('test_a_foo')
        test.set_test_name_and_assignment()
        self.assertEqual(test.result_assignment, "Assignment1")
        self.assertEqual(test.result_test_name, "foo")



    def test_set_test_name_and_assignment_rasie_exception_missing_identifier(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when test function
        miss identifier after letter.
        """
        class TestAssignment1(ExamTestCase):
            def test_a(self):
                pass

        test = TestAssignment1('test_a')
        with self.assertRaises(ValueError) as cxt:
            test.set_test_name_and_assignment()

        self.assertEqual(test.result_assignment, "Assignment1")
        with self.assertRaises(AttributeError) as cxt:
            self.assertEqual(test.result_test_name, "foo")



    def test_set_test_name_and_assignment_rasie_exception_missing_lettert(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when test function
        miss letter.
        """
        class TestAssignment1(ExamTestCase):
            def test_foo(self):
                pass

        test = TestAssignment1('test_foo')
        with self.assertRaises(ValueError) as cxt:
            test.set_test_name_and_assignment()

        self.assertEqual(test.result_assignment, "Assignment1")
        with self.assertRaises(AttributeError) as cxt:
            self.assertEqual(test.result_test_name, "foo")



    def test_set_test_name_and_assignment_rasie_exception_missing_assignment(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when class name
        miss "Assignment".
        """
        class Testassignment1(ExamTestCase):
            def test_a_foo(self):
                pass

        test = Testassignment1('test_a_foo')
        with self.assertRaises(ValueError) as cxt:
            test.set_test_name_and_assignment()
        with self.assertRaises(AttributeError) as cxt:
            self.assertEqual(test.result_test_name, "foo")



    def test_set_test_name_and_assignment_rasie_exception_missing_number(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when class name
        number is missing.
        """
        class TestAssignment(ExamTestCase):
            def test_a_foo(self):
                pass

        test = TestAssignment('test_a_foo')
        with self.assertRaises(ValueError) as cxt:
            test.set_test_name_and_assignment()
        with self.assertRaises(AttributeError) as cxt:
            self.assertEqual(test.result_test_name, "foo")



if __name__ == '__main__':
    # runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(verbosity=2)
