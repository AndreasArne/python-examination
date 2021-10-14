"""
Overriding TestCase for exam tool.
"""
from examiner import ExamTestCase

class ExamTestCaseExam(ExamTestCase):
    """
    Custom class for examination.
    Can set points for assignments and a threshold for passing.
    """

    points_for_pass = 0

    def __init__(self, points_worth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points_worth = points_worth
