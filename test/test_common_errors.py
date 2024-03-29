"""
Use this to test our new and added functionality.
"""
import sys
import os
import unittest
import traceback
from io import StringIO
from unittest import mock
from unittest.mock import patch
from examiner import common_errors, exceptions as exce, ExamTestCase, tags

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



    def test_wrong_nr_of_input_calls_found_dynamic(self):
        class Test1InputError(ExamTestCase):
            def test_a(self):
                "comment"
                inp = ["test"]
                with patch('builtins.input', side_effect=inp):
                    with patch('sys.stdout', new=StringIO()) as fake_out:
                        _ = input("ok")
                        _ = input("too  many")
                        str_data = fake_out.getvalue()
        test = Test1InputError('test_a')
        try:
            test.test_a()
        except StopIteration as e:
            tb = traceback.TracebackException(type(e), e, e.__traceback__, limit=None)
            res = common_errors.wrong_nr_of_input_calls(tb)
        self.assertIn("Tips!", res)
