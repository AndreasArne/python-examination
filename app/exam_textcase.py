"""
Test Case implementaion for exam tool.
"""
import unittest
from unittest.util import safe_repr

class ExamTestCase(unittest.TestCase):
    """
    Override method to customize outputs of testcases.
    """

    def set_answer(self, student_answer, correct_answer):
        """
        Set students answer and correct answer as members.
        """
        self.student_answer = student_answer
        self.correct_answer = correct_answer



    def assertIn(self, member, container, msg=None):
        """Check if value in container. Container comes from student"""
        self.set_answer(container, member)
        super().assertIn(member, container, msg)



    def assertTrue(self, expr, msg=None):
        """Check that the expression is true."""
        self.set_answer(expr, True)
        super().assertTrue(expr, msg)
