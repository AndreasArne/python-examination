"""
Overriding TestCase for exam tool.
"""
import re
import unittest
from app import helper_functions as hf

class ExamTestCase(unittest.TestCase):
    """
    Override methods to help customize outputs of testcases.
    """

    ASSIGNMENT_REGEX = r".*Test(Assignment[0-9]+)\)"
    TEST_NAME_REGEX = r"test_[a-z]_(\w+) "



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignment = ""
        self.test_name = ""
        self.student_answer = ""
        self.correct_answer = ""
        self._set_test_name_and_assignment()



    def _set_test_name_and_assignment(self):
        """
        Extract Assignment from TestCase name.
        Extract test name from test function name.
        Format testname and assignment text and assign to test object.
        """
        test_string = str(self)
        try:
            self.assignment = re.search(self.ASSIGNMENT_REGEX, test_string).group(1)
        except AttributeError as e:
            raise ValueError("Class name for TestCase should follow the structure 'TestAssignment<number>'") from e

        try:
            self.test_name = re.search(self.TEST_NAME_REGEX, test_string).group(1).replace("_", " ")
        except AttributeError as e:
            raise ValueError("Test function name should follow the structure 'test_<letter>_<name>'") from e



    def set_answers(self, student_answer, correct_answer, options=None):
        """
        Set students answer and correct answer as members.
        """
        self.student_answer = repr(student_answer)
        self.correct_answer = repr(correct_answer)
        if options is not None:
            if "norepr" in options:
                if isinstance(student_answer, str):
                    self.student_answer = hf.clean_str(student_answer)
                else:
                    self.student_answer = str(student_answer)


    def assertEqual(self, first, second, msg=None):
        """
        Check if first is equal to second. Save correct and student answer as to variables.
        First comes from student
        """
        self.set_answers(first, second)
        super().assertEqual(first, second, msg)



    def assertIn(self, member, container, msg=None):
        """
        Check if value in container.  Save correct and student answer as to variables.
        Container comes from student
        """
        self.set_answers(container, member, msg)
        super().assertIn(member, container, msg)



    def assertFalse(self, expr, msg=None):
        """
        Check that the expression is False.
        Save correct and student answer as to variables.
        """
        self.set_answers(expr, False)
        super().assertFalse(expr, msg)



    def assertTrue(self, expr, msg=None):
        """
        Check that the expression is true.
        Save correct and student answer as to variables.
        """
        self.set_answers(expr, True)
        super().assertTrue(expr, msg)
