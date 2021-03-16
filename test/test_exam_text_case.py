"""
Use this to test our new and added functionality.
"""
import sys
import unittest
from unittest.runner import _WritelnDecorator

import examiner.exceptions as exce
from examiner.exam_test_case import ExamTestCase




class Test_ExamTestCase(unittest.TestCase):

    def setup_empty_examtextcase(self):
        class Test1Assignment1(ExamTestCase):
            def test_a_foo(self):
                pass
        return Test1Assignment1("test_a_foo")



    def test_set_answer_strings(self):
        """
        Answers are strings and called with no options
        Test that special chars in string are excaped
        """
        test = self.setup_empty_examtextcase()
        test.set_answers("\[ 32 m a string\n", "another string")
        self.assertEqual(test.student_answer, "'\\\\[ 32 m a string\\n'")
        self.assertEqual(test.correct_answer, "'another string'")



    def test_set_answer_list(self):
        """
        Answers are lists and with no options
        """
        test = self.setup_empty_examtextcase()
        test.set_answers(["a string", 1], ["another string", 3.2, True])
        self.assertEqual(test.student_answer, "['a string', 1]")
        self.assertEqual(test.correct_answer, "['another string', 3.2, True]")



    def test_set_answer_strings_norepr(self):
        """
        Called with option norepr
        Test that special chars are not escaped
        """
        test = self.setup_empty_examtextcase()
        test.norepr = True
        test.set_answers("\[ 32 m a string\n", "another string")
        self.assertEqual(test.student_answer, "\\[ 32 m a string\n")
        self.assertEqual(test.correct_answer, "'another string'")



    def test_set_answer_list(self):
        """
        Answers are lists and with no options
        """
        test = self.setup_empty_examtextcase()
        test.norepr = True
        test.set_answers(
            ["a string", 1],
            ["another string", 3.2, True],
        )
        self.assertEqual(test.student_answer, "['a string', 1]")
        self.assertEqual(test.correct_answer, "['another string', 3.2, True]")



    def test_set_answer_norepr_clean(self):
        """
        Called with option norepr and that clean works
        """
        test = self.setup_empty_examtextcase()
        test.norepr = True
        test.set_answers(
            chr(27) + "[2J" + chr(27) + "[;H" + "a string",
            "another string"
        )
        self.assertEqual(test.student_answer, "a string")
        self.assertEqual(test.correct_answer, "'another string'")



    def test_set_test_name_and_assignment(self):
        """
        Tests that set_test_name_and_assignment extracts test name and assignment
        correct.
        """
        class Test1Assignment1(ExamTestCase):
            def test_a_foo(self):
                pass

        test = Test1Assignment1('test_a_foo')
        self.assertEqual(test.assignment, "Assignment1")
        self.assertEqual(test.test_name, "foo")



    def test_set_assignment_rasie_exception_missing_identifier(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when test function
        miss identifier after letter.
        """
        class Test2Assignment1(ExamTestCase):
            def test_a(self):
                pass

        with self.assertRaises(exce.TestFuncNameError) as cxt:
            test = Test2Assignment1('test_a')



    def test_set_assignment_rasie_exception_missing_lettert(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when test function
        miss letter.
        """
        class Test1Assignment1(ExamTestCase):
            def test_foo(self):
                pass

        with self.assertRaises(exce.TestFuncNameError) as cxt:
            test = Test1Assignment1('test_foo')



    def test_set_assignment_rasie_exception_missing_Upper_letter(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when class name
        miss word that start with uppercase letter.
        """
        class Test1assignment(ExamTestCase):
            def test_a_foo(self):
                pass

        with self.assertRaises(exce.TestClassNameError) as cxt:
            test = Test1assignment('test_a_foo')



    def test_set_assignment_rasie_exception_missing_number(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when class name
        miss start number.
        """
        class TestAssignment1(ExamTestCase):
            def test_a_foo(self):
                pass

        with self.assertRaises(exce.TestClassNameError) as cxt:
            test = TestAssignment1('test_a_foo')



    def test_set_assignment_works_without_number_after(self):
        """
        Tests that set_test_name_and_assignment work with number after word.
        """
        class Test1Assignment(ExamTestCase):
            def test_a_foo(self):
                pass

        test = Test1Assignment('test_a_foo')
        self.assertEqual(test.assignment, "Assignment")
        self.assertEqual(test.test_name, "foo")



    def test_set_assignment_works_with_multiple_words(self):
        """
        Tests that set_test_name_and_assignment work with multiple words.
        """
        class Test4ModulesExist(ExamTestCase):
            def test_a_foo(self):
                pass

        test = Test4ModulesExist('test_a_foo')
        self.assertEqual(test.assignment, "ModulesExist")
        self.assertEqual(test.test_name, "foo")



if __name__ == '__main__':
    # runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(verbosity=2)
