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
from app.exam_textcase import ExamTestCase
from app.exam_test_result import ExamTestResult

proj_path = os.path.dirname(os.path.realpath(__file__ + "/.."))
if proj_path not in sys.path:
    sys.path.insert(0, proj_path)
#pylint: disable=wrong-import-position
import main
#pylint: enable=wrong-import-position
#pylint: disable=attribute-defined-outside-init, line-too-long


class TestAssignment1(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.

    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """

    def test_a_module(self):
        """
        Testar att din kod är uppdelad i rätt modler.
        |G|Förväntar att följande modul finns men hittades inte:|/RE|
        {arguments}
        
        """
        self._argument = "main"
        self.assertIsNotNone(util.find_spec(self._argument))
        self._argument = "menu"
        self.assertIsNotNone(util.find_spec(self._argument))
        self._argument = "analyzer"
        self.assertIsNotNone(util.find_spec(self._argument))
    # 
    # def test_b_analyzer(self):
    #     """
    #     Test analyzer
    #     """
    #     with patch('builtins.input', side_effect=["lines", "q"]):
    #         with patch('sys.stdout', new=StringIO()) as fake_out:
    #             main.main()
    #             str_data = fake_out.getvalue()
    #             self.assertIn("17", str_data)
    # 
    #     with patch('builtins.input', side_effect=["words", "q"]):
    #         with patch('sys.stdout', new=StringIO()) as fake_out:
    #             main.main()
    #             str_data = fake_out.getvalue()
    #             self.assertIn("199", str_data)
    # 
    #     with patch('builtins.input', side_effect=["letters", "q"]):
    #         with patch('sys.stdout', new=StringIO()) as fake_out:
    #             main.main()
    #             str_data = fake_out.getvalue()
    #             self.assertIn("907", str_data)
    # 
    #     with patch('builtins.input', side_effect=["word_frequency", "q"]):
    #         with patch('sys.stdout', new=StringIO()) as fake_out:
    #             main.main()
    #             str_data = fake_out.getvalue()
    #             self.assertIn("the", str_data)
    #             self.assertIn("6.0%", str_data)
    # 
    #     with patch('builtins.input', side_effect=["letter_frequency", "q"]):
    #         with patch('sys.stdout', new=StringIO()) as fake_out:
    #             main.main()
    #             str_data = fake_out.getvalue()
    #             self.assertIn("11.9%", str_data)
    #             self.assertIn("7.1%", str_data)
    # 
    #     with patch('builtins.input', side_effect=["all", "q"]):
    #         with patch('sys.stdout', new=StringIO()) as fake_out:
    #             main.main()
    #             str_data = fake_out.getvalue()
    #             self.assertIn("17", str_data)
    #             self.assertIn("199", str_data)
    #             self.assertIn("907", str_data)
    #             self.assertIn("the", str_data)
    #             self.assertIn("6.0%", str_data)
    #             self.assertIn("11.9%", str_data)
    #             self.assertIn("7.1%", str_data)

if __name__ == '__main__':
    runner = TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(testRunner=runner, exit=False)
