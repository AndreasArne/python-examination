"""
Use this to test our new and added functionality.
"""
import sys
import os
import unittest
from unittest.runner import _WritelnDecorator
from unittest import SkipTest

# proj_path = os.path.dirname(os.path.realpath(__file__ + "/../"))
# path = proj_path + "/examiner"
# if path not in sys.path:
#     sys.path.insert(0, path)

from examiner import exceptions as exce
from examiner import ExamTestCase
from examiner import tags

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



    def test_set_answer_list_two(self):
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
            link_to_assignment = "a link"
            def test_a_foo(self):
                pass

        test = Test1Assignment1('test_a_foo')
        self.assertEqual(test.assignment, "Assignment1")
        self.assertEqual(test.test_name, "foo")
        self.assertEqual(test.link_to_assignment, "a link")



    def test_set_assignment_only_a_letter_for_func_name(self):
        """
        Tests that set_test_name_and_assignment work for only a letter after test_.
        """
        class Test2Assignment1(ExamTestCase):
            def test_a(self):
                pass

        test = Test2Assignment1('test_a')
        self.assertEqual(test.assignment, "Assignment1")
        self.assertEqual(test.test_name, "a")
        self.assertEqual(test.link_to_assignment, "")


    def test_set_assignment_rasie_exception_missing_letter(self):
        """
        Tests that set_test_name_and_assignment raise ValueError when test function
        miss letter.
        """
        class Test1Assignment1(ExamTestCase):
            def test_foo(self):
                pass

        test = Test1Assignment1('test_foo')
        self.assertEqual(test.assignment, "Assignment1")
        self.assertEqual(test.test_name, "foo")



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

        test = TestAssignment1('test_a_foo')
        self.assertEqual(test.assignment, "Assignment1")
        self.assertEqual(test.test_name, "foo")


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



    def test_skip_test_by_tags(self):
        """
        Tests that SkipTest is raised when the tags does not match.
        """
        class Test1Tags1(ExamTestCase):
            USER_TAGS = ["dont_skip"]

            @tags("skip")
            def test_a_foo(self):
                self.assertEqual('correct', 'incorrect')

        test = Test1Tags1('test_a_foo')

        with self.assertRaises(SkipTest) as _:
            test.test_a_foo()
        # check that method was decorated for tags
        self.assertEqual(getattr(test.test_a_foo, "__wrapped__").__name__, "test_a_foo")



    def test_run_test_by_tags(self):
        """
        Tests that an overwritten test runs the test without being skipped.
        """
        class Test1Tags1(ExamTestCase):
            USER_TAGS = ["dont_skip"]

            @tags("dont_skip")
            def test_a_foo(self):
                return "Not Skipped"

        test = Test1Tags1('test_a_foo')
        self.assertEqual(test.test_a_foo(), "Not Skipped")
        # check that method was decorated for tags
        self.assertEqual(getattr(test.test_a_foo, "__wrapped__").__name__, "test_a_foo")


    def test_skip_test_when_error(self):
        """
        Tests that SkipTest is raised when tested code raise an exception.
        This was a bug before.
        """
        class Test1Tags1(ExamTestCase):
            USER_TAGS = ["dont_skip"]

            @tags("skip")
            def test_a_foo(self):
                raise KeyError()

        test = Test1Tags1('test_a_foo')

        with self.assertRaises(SkipTest) as _:
            test.test_a_foo()

    def test_passing_simpel_test(self):
        """
        Check that a normal test works
        """
        class Test1Simpel(ExamTestCase):

            def test_a_foo(self):
                self.assertEqual("hej", "hej")

        test = Test1Simpel('test_a_foo')
        self.assertEqual(test.USER_TAGS, [])


    def test_wrapped_tags_correct_metadata(self):
        """
        Check that a tags-wrapped test has its own metadata and not wrapped functions
        """
        class Test1Simpel(ExamTestCase):

            @tags("test")
            def test_a_foo(self):
                """a comment"""
                self.assertEqual("hej", "hej")

        test = Test1Simpel('test_a_foo')
        self.assertEqual(test._testMethodDoc, "a comment")

if __name__ == '__main__':
    # runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(verbosity=2)
