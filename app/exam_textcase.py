"""
Overriding TestCase for exam tool.
"""
import unittest

class ExamTestCase(unittest.TestCase):
    """
    Override methods to help customize outputs of testcases.
    """

    def set_answers(self, student_answer, correct_answer):
        """
        Set students answer and correct answer as members.
        """
        self.student_answer = repr(student_answer)
        self.correct_answer = repr(correct_answer)



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
        self.set_answers(container, member)
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
