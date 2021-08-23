"""
Use this to test our new and added functionality.
"""
import sys
import os
import unittest
from unittest import mock
from examiner import common_errors

# proj_path = os.path.dirname(os.path.realpath(__file__ + "/../"))
# path = proj_path + "/examiner"
# if path not in sys.path:
#     sys.path.insert(0, path)

class TestCheckIfCommonError(unittest.TestCase):
    def test_return_false_if_missing_exception(self):
        res = common_errors.check_if_common_error("MissingException", "", "")
        self.assertFalse(res)

    def test_return_msg_for_found_error(self):
        with mock.patch("examiner.common_errors.wrong_nr_of_input_calls", return_value="msg"):
            res = common_errors.check_if_common_error("StopIteration", "", "")
        self.assertIn("msg", res)

    def test_return_false_for_not_common_error(self):
        with mock.patch("examiner.common_errors.wrong_nr_of_input_calls", return_value=False):
            res = common_errors.check_if_common_error("StopIteration", "", "")
        self.assertFalse(res)

class TestErrorFunctions(unittest.TestCase):


    def test_assertion_traceback(self):
        tb_mock = mock.MagicMock()
        tb_mock.format.return_value = [
            'Traceback (most recent call last):',
            'File "/c/Users/aar/git/python-dev/.dbwebb/test/examiner/helper_functions.py", line 173, in wrapper',
            'return f(self, *args, **kwargs)',
            'File "/c/Users/aar/git/python-dev/.dbwebb/test/examiner/exam_test_case.py", line 87, in assertIn',
            'super().assertIn(member, container, msg)',
            'AssertionError: 1 != 2',
        ]
        with mock.patch("examiner.common_errors.ARGS.trace_assertion_error", True):
            res = common_errors.check_if_common_error("AssertionError", tb_mock, "")
        self.assertIn('AssertionError: 1 != 2', res)
        self.assertTrue(isinstance(res, str))



    def test_assertion_traceback_trace_false(self):
        tb_mock = mock.MagicMock()

        with mock.patch("examiner.common_errors.ARGS.trace_assertion_error", False):
            res = common_errors.check_if_common_error("AssertionError", tb_mock, "")
            self.assertEqual("", res)



    def test_wrong_nr_of_input_calls_found(self):
        tb_mock = mock.MagicMock()
        stack_obj_mock2 = mock.MagicMock()
        stack_obj_mock2.line = "temp = input('Enter current outside temperature')"
        stack_obj_mock3 = mock.MagicMock()
        stack_obj_mock3.line = "return _mock_self._mock_call(*args, **kwargs)"
        stack_obj_mock4 = mock.MagicMock()
        stack_obj_mock4.line = "result = next(effect)"

        tb_mock.stack = [
            "",
            "",
            stack_obj_mock2,
            stack_obj_mock3,
            stack_obj_mock4,
        ]
        res = common_errors.wrong_nr_of_input_calls(tb_mock)
        self.assertIn("(Tips!", res)

    def test_wrong_nr_of_input_calls_not_found(self):
        tb_mock = mock.MagicMock()
        stack_obj_mock2 = mock.MagicMock()
        stack_obj_mock2.line = "temp = input('Enter current outside temperature')"
        stack_obj_mock3 = mock.MagicMock()
        stack_obj_mock3.line = "some some"
        stack_obj_mock4 = mock.MagicMock()
        stack_obj_mock4.line = "result = next(effect)"

        tb_mock.stack = [
            "",
            "",
            stack_obj_mock2,
            stack_obj_mock3,
            stack_obj_mock4,
        ]
        res = common_errors.wrong_nr_of_input_calls(tb_mock)
        self.assertFalse(res)
