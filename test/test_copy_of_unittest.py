"""
Rewrite of
https://github.com/python/cpython/blob/48fbe52ac71ea711a4701db909ad1ce2647b09fd/Lib/unittest/test/test_result.py
to use our changed TextTestResult class.
Used to have a clue if we break original functionality of the result class.
"""

import io
import sys
import textwrap

# from test import support

import traceback
import unittest

from unittest import mock
from unittest.runner import _WritelnDecorator
from app.exam_test_result import ExamTestResult


class MockTraceback(object):
    class TracebackException:
        def __init__(self, *args, **kwargs):
            self.capture_locals = kwargs.get('capture_locals', False)
        def format(self):
            result = ['A traceback']
            if self.capture_locals:
                result.append('locals')
            return result

def restore_traceback():
    unittest.result.traceback = traceback


class Test_TestResult(unittest.TestCase):
    # Note: there are not separate tests for TestResult.wasSuccessful(),
    # TestResult.errors, TestResult.failures, TestResult.testsRun or
    # TestResult.shouldStop because these only have meaning in terms of
    # other TestResult methods.
    #
    # Accordingly, tests for the aforenamed attributes are incorporated
    # in with the tests for the defining methods.
    ################################################################

    def test_init(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)

        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 0)
        self.assertEqual(result.shouldStop, False)
        self.assertIsNone(result._stdout_buffer)
        self.assertIsNone(result._stderr_buffer)

    # "This method can be called to signal that the set of tests being
    # run should be aborted by setting the TestResult's shouldStop
    # attribute to True."
    def test_stop(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)

        result.stop()

        self.assertEqual(result.shouldStop, True)

    # "Called when the test case test is about to be run. The default
    # implementation simply increments the instance's testsRun counter."
    def test_startTest(self):
        """
        Changed name of "test_1" to "test_a_foo". To match requirement of test names.
        """
        class TestAssignment1(unittest.TestCase):
            def test_a_foo(self):
                pass

        test = TestAssignment1('test_a_foo')

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)

        result.startTest(test)

        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        result.stopTest(test)

    # "Called after the test case test has been executed, regardless of
    # the outcome. The default implementation does nothing."
    def test_stopTest(self):
        class TestAssignment1(unittest.TestCase):
            def test_a_foo(self):
                pass

        test = TestAssignment1('test_a_foo')

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)


        result.startTest(test)

        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        result.stopTest(test)

        # Same tests as above; make sure nothing has changed
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

    # "Called before and after tests are run. The default implementation does nothing."
    def test_startTestRun_stopTestRun(self):
        result = unittest.TestResult()
        result.startTestRun()
        result.stopTestRun()

    # "addSuccess(test)"
    # ...
    # "Called when the test case test succeeds"
    # ...
    # "wasSuccessful() - Returns True if all tests run so far have passed,
    # otherwise returns False"
    # ...
    # "testsRun - The total number of tests run so far."
    # ...
    # "errors - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test which raised an
    # unexpected exception. Contains formatted
    # tracebacks instead of sys.exc_info() results."
    # ...
    # "failures - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test where a failure was
    # explicitly signalled using the TestCase.fail*() or TestCase.assert*()
    # methods. Contains formatted tracebacks instead
    # of sys.exc_info() results."
    def test_addSuccess(self):
        class TestAssignment1(unittest.TestCase):
            def test_a_foo(self):
                pass

        test = TestAssignment1('test_a_foo')

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)


        result.startTest(test)
        result.addSuccess(test)
        result.stopTest(test)

        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

    # "addFailure(test, err)"
    # ...
    # "Called when the test case test signals a failure. err is a tuple of
    # the form returned by sys.exc_info(): (type, value, traceback)"
    # ...
    # "wasSuccessful() - Returns True if all tests run so far have passed,
    # otherwise returns False"
    # ...
    # "testsRun - The total number of tests run so far."
    # ...
    # "errors - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test which raised an
    # unexpected exception. Contains formatted
    # tracebacks instead of sys.exc_info() results."
    # ...
    # "failures - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test where a failure was
    # explicitly signalled using the TestCase.fail*() or TestCase.assert*()
    # methods. Contains formatted tracebacks instead
    # of sys.exc_info() results."
    def test_addFailure(self):
        class TestAssignment1(unittest.TestCase):
            def test_a_foo(self):
                """
                A simple test that is supposed to fail.
                """
                pass

        test = TestAssignment1('test_a_foo')
        try:
            test.fail("foo")
        except:
            exc_info_tuple = sys.exc_info()

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)

        result.startTest(test)
        result.addFailure(test, exc_info_tuple)
        result.stopTest(test)

        self.assertFalse(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        test_case, formatted_exc = result.failures[0]
        self.assertIs(test_case, test)
        self.assertIsInstance(formatted_exc, str)

    # "addError(test, err)"
    # ...
    # "Called when the test case test raises an unexpected exception err
    # is a tuple of the form returned by sys.exc_info():
    # (type, value, traceback)"
    # ...
    # "wasSuccessful() - Returns True if all tests run so far have passed,
    # otherwise returns False"
    # ...
    # "testsRun - The total number of tests run so far."
    # ...
    # "errors - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test which raised an
    # unexpected exception. Contains formatted
    # tracebacks instead of sys.exc_info() results."
    # ...
    # "failures - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test where a failure was
    # explicitly signalled using the TestCase.fail*() or TestCase.assert*()
    # methods. Contains formatted tracebacks instead
    # of sys.exc_info() results."
    def test_addError(self):
        class TestAssignment1(unittest.TestCase):
            def test_a_foo(self):
                pass

        test = TestAssignment1('test_a_foo')
        try:
            raise TypeError()
        except:
            exc_info_tuple = sys.exc_info()

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)

        result.startTest(test)
        result.addError(test, exc_info_tuple)
        result.stopTest(test)

        self.assertFalse(result.wasSuccessful())
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        test_case, formatted_exc = result.errors[0]
        self.assertIs(test_case, test)
        self.assertIsInstance(formatted_exc, str)

    def test_addError_locals(self):
        class TestAssignment1(unittest.TestCase):
            def test_a_foo(self):
                1/0

        test = TestAssignment1('test_a_foo')
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)

        result.tb_locals = True
        with mock.patch('app.exam_test_result.traceback') as m_tb:
            m_tb.TracebackException = MockTraceback.TracebackException

            self.addCleanup(restore_traceback)
            result.startTestRun()
            test.run(result)
            result.stopTestRun()

        self.assertEqual(len(result.errors), 1)
        test_case, formatted_exc = result.errors[0]
        self.assertEqual('A tracebacklocals', formatted_exc)

    def test_addSubTest(self):
        class TestAssignment1(unittest.TestCase):
            def test_a_foo(self):
                """
                A simple test that is supposed to fail.
                """
                nonlocal subtest
                with self.subTest(foo=1):
                    subtest = self._subtest
                    try:
                        1/0
                    except ZeroDivisionError:
                        exc_info_tuple = sys.exc_info()
                    # Register an error by hand (to check the API)
                    result.addSubTest(test, subtest, exc_info_tuple)
                    # Now trigger a failure
                    self.fail("some recognizable failure")

        subtest = None
        test = TestAssignment1('test_a_foo')
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)

        test.run(result)

        self.assertFalse(result.wasSuccessful())
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        test_case, formatted_exc = result.errors[0]
        self.assertIs(test_case, subtest)
        self.assertIn("ZeroDivisionError", formatted_exc)
        test_case, formatted_exc = result.failures[0]
        self.assertIs(test_case, subtest)
        self.assertIn("A simple test that is supposed to fail.", formatted_exc)

    def testGetDescriptionWithoutDocstring(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)
        self.assertEqual(
                result.getDescription(self),
                'testGetDescriptionWithoutDocstring (' + __name__ +
                '.Test_TestResult)')

    def testGetSubTestDescriptionWithoutDocstring(self):
        with self.subTest(foo=1, bar=2):
            # result = unittest.TextTestResult(None, True, 1)
            result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
            self.assertEqual(
                    result.getDescription(self._subtest),
                    'testGetSubTestDescriptionWithoutDocstring (' + __name__ +
                    '.Test_TestResult) (bar=2, foo=1)')
        with self.subTest('some message'):
            # result = unittest.TextTestResult(None, True, 1)
            result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
            self.assertEqual(
                    result.getDescription(self._subtest),
                    'testGetSubTestDescriptionWithoutDocstring (' + __name__ +
                    '.Test_TestResult) [some message]')

    def testGetSubTestDescriptionWithoutDocstringAndParams(self):
        with self.subTest():
            result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
            self.assertEqual(
                    result.getDescription(self._subtest),
                    'testGetSubTestDescriptionWithoutDocstringAndParams '
                    '(' + __name__ + '.Test_TestResult) (<subtest>)')

    def testGetSubTestDescriptionForFalsyValues(self):
        expected = 'testGetSubTestDescriptionForFalsyValues (%s.Test_TestResult) [%s]'
        result = unittest.TextTestResult(None, True, 1)

        for arg in [0, None, []]:
            with self.subTest(arg):
                self.assertEqual(
                    result.getDescription(self._subtest),
                    expected % (__name__, arg)
                )

    def testGetNestedSubTestDescriptionWithoutDocstring(self):
        with self.subTest(foo=1):
            with self.subTest(baz=2, bar=3):
                result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
                self.assertEqual(
                        result.getDescription(self._subtest),
                        'testGetNestedSubTestDescriptionWithoutDocstring '
                        '(' + __name__ + '.Test_TestResult) (bar=3, baz=2, foo=1)')

    def testGetDuplicatedNestedSubTestDescriptionWithoutDocstring(self):
        with self.subTest(foo=1, bar=2):
            with self.subTest(bar=3, baz=4):
                result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
                self.assertEqual(
                        result.getDescription(self._subtest),
                        'testGetDuplicatedNestedSubTestDescriptionWithoutDocstring '
                        '(' + __name__ + '.Test_TestResult) (bar=3, baz=4, foo=1)')

    @unittest.skipIf(sys.flags.optimize >= 2,
                     "Docstrings are omitted with -O2 and above")
    def testGetDescriptionWithOneLineDocstring(self):
        """Tests getDescription() for a method with a docstring."""
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        self.assertEqual(
                result.getDescription(self),
               ('testGetDescriptionWithOneLineDocstring '
                '(' + __name__ + '.Test_TestResult)\n'
                'Tests getDescription() for a method with a docstring.'))

    @unittest.skipIf(sys.flags.optimize >= 2,
                     "Docstrings are omitted with -O2 and above")
    def testGetSubTestDescriptionWithOneLineDocstring(self):
        """Tests getDescription() for a method with a docstring."""
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        with self.subTest(foo=1, bar=2):
            self.assertEqual(
                result.getDescription(self._subtest),
               ('testGetSubTestDescriptionWithOneLineDocstring '
                '(' + __name__ + '.Test_TestResult) (bar=2, foo=1)\n'
                'Tests getDescription() for a method with a docstring.'))

    @unittest.skipIf(sys.flags.optimize >= 2,
                     "Docstrings are omitted with -O2 and above")
    def testGetDescriptionWithMultiLineDocstring(self):
        """Tests getDescription() for a method with a longer docstring.
        The second line of the docstring.
        """
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        self.assertEqual(
                result.getDescription(self),
               ('testGetDescriptionWithMultiLineDocstring '
                '(' + __name__ + '.Test_TestResult)\n'
                'Tests getDescription() for a method with a longer '
                'docstring.'))

    @unittest.skipIf(sys.flags.optimize >= 2,
                     "Docstrings are omitted with -O2 and above")
    def testGetSubTestDescriptionWithMultiLineDocstring(self):
        """Tests getDescription() for a method with a longer docstring.
        The second line of the docstring.
        """
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        with self.subTest(foo=1, bar=2):
            self.assertEqual(
                result.getDescription(self._subtest),
               ('testGetSubTestDescriptionWithMultiLineDocstring '
                '(' + __name__ + '.Test_TestResult) (bar=2, foo=1)\n'
                'Tests getDescription() for a method with a longer '
                'docstring.'))

    def testStackFrameTrimming(self):
        class Frame(object):
            class tb_frame(object):
                f_globals = {}
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        self.assertFalse(result._is_relevant_tb_level(Frame))

        Frame.tb_frame.f_globals['__unittest'] = True
        self.assertTrue(result._is_relevant_tb_level(Frame))

    def testFailFast(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        result._exc_info_to_string = lambda *_: ''
        result.failfast = True
        result.addError(None, None)
        self.assertTrue(result.shouldStop)

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        result._exc_info_to_string = lambda *_: ''
        result.failfast = True
        result.addFailure(None, None)
        self.assertTrue(result.shouldStop)

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        result._exc_info_to_string = lambda *_: ''
        result.failfast = True
        result.addUnexpectedSuccess(None)
        self.assertTrue(result.shouldStop)

    def testFailFastSetByRunner(self):
        runner = unittest.TextTestRunner(stream=io.StringIO(), failfast=True)
        def test(result):
            self.assertTrue(result.failfast)
        result = runner.run(test)



class TestOutputBuffering(unittest.TestCase):

    def setUp(self):
        self._real_out = sys.stdout
        self._real_err = sys.stderr

    def tearDown(self):
        sys.stdout = self._real_out
        sys.stderr = self._real_err

    def testBufferOutputOff(self):
        real_out = self._real_out
        real_err = self._real_err

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        self.assertFalse(result.buffer)

        self.assertIs(real_out, sys.stdout)
        self.assertIs(real_err, sys.stderr)

        result.startTest(self)

        self.assertIs(real_out, sys.stdout)
        self.assertIs(real_err, sys.stderr)

    def testBufferOutputStartTestAddSuccess(self):
        real_out = self._real_out
        real_err = self._real_err

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        self.assertFalse(result.buffer)

        result.buffer = True

        self.assertIs(real_out, sys.stdout)
        self.assertIs(real_err, sys.stderr)

        result.startTest(self)

        self.assertIsNot(real_out, sys.stdout)
        self.assertIsNot(real_err, sys.stderr)
        self.assertIsInstance(sys.stdout, io.StringIO)
        self.assertIsInstance(sys.stderr, io.StringIO)
        self.assertIsNot(sys.stdout, sys.stderr)

        out_stream = sys.stdout
        err_stream = sys.stderr

        result._original_stdout = io.StringIO()
        result._original_stderr = io.StringIO()

        print('foo')
        print('bar', file=sys.stderr)

        self.assertEqual(out_stream.getvalue(), 'foo\n')
        self.assertEqual(err_stream.getvalue(), 'bar\n')

        self.assertEqual(result._original_stdout.getvalue(), '')
        self.assertEqual(result._original_stderr.getvalue(), '')

        result.addSuccess(self)
        result.stopTest(self)

        self.assertIs(sys.stdout, result._original_stdout)
        self.assertIs(sys.stderr, result._original_stderr)

        self.assertEqual(result._original_stdout.getvalue(), '')
        self.assertEqual(result._original_stderr.getvalue(), '')

        self.assertEqual(out_stream.getvalue(), '')
        self.assertEqual(err_stream.getvalue(), '')


    def getStartedResult(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        result.buffer = True
        result.startTest(self)
        return result

    def testBufferOutputAddErrorOrFailure(self):
        unittest.result.traceback = MockTraceback
        self.addCleanup(restore_traceback)

        for message_attr, add_attr, include_error in [
            ('errors', 'addError', True),
            ('failures', 'addFailure', False),
            ('errors', 'addError', True),
            ('failures', 'addFailure', False)
        ]:
            result = self.getStartedResult()
            buffered_out = sys.stdout
            buffered_err = sys.stderr
            result._original_stdout = io.StringIO()
            result._original_stderr = io.StringIO()

            print('foo', file=sys.stdout)
            if include_error:
                print('bar', file=sys.stderr)


            addFunction = getattr(result, add_attr)
            addFunction(self, (None, None, None))
            result.stopTest(self)

            result_list = getattr(result, message_attr)
            self.assertEqual(len(result_list), 1)

            test, message = result_list[0]
            expectedOutMessage = textwrap.dedent("""
                Stdout:
                foo
            """)
            expectedErrMessage = ''
            if include_error:
                expectedErrMessage = textwrap.dedent("""
                Stderr:
                bar
            """)

            expectedFullMessage = 'None: None\n%s%s' % (expectedOutMessage, expectedErrMessage)

            self.assertIs(test, self)
            self.assertEqual(result._original_stdout.getvalue(), expectedOutMessage)
            self.assertEqual(result._original_stderr.getvalue(), expectedErrMessage)
            self.assertMultiLineEqual(message, expectedFullMessage)

    def testBufferSetupClass(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        result.buffer = True

        class Foo(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                1/0
            def test_foo(self):
                pass
        suite = unittest.TestSuite([Foo('test_foo')])
        suite(result)
        self.assertEqual(len(result.errors), 1)

    def testBufferTearDownClass(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        result.buffer = True

        class Foo(unittest.TestCase):
            @classmethod
            def tearDownClass(cls):
                1/0
            def test_foo(self):
                pass
        suite = unittest.TestSuite([Foo('test_foo')])
        suite(result)
        self.assertEqual(len(result.errors), 1)

    def testBufferSetUpModule(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        result.buffer = True

        class Foo(unittest.TestCase):
            def test_foo(self):
                pass
        class Module(object):
            @staticmethod
            def setUpModule():
                1/0

        Foo.__module__ = 'Module'
        sys.modules['Module'] = Module
        self.addCleanup(sys.modules.pop, 'Module')
        suite = unittest.TestSuite([Foo('test_foo')])
        suite(result)
        self.assertEqual(len(result.errors), 1)

    def testBufferTearDownModule(self):
        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 1)
        result.buffer = True

        class Foo(unittest.TestCase):
            def test_foo(self):
                pass
        class Module(object):
            @staticmethod
            def tearDownModule():
                1/0

        Foo.__module__ = 'Module'
        sys.modules['Module'] = Module
        self.addCleanup(sys.modules.pop, 'Module')
        suite = unittest.TestSuite([Foo('test_foo')])
        suite(result)
        self.assertEqual(len(result.errors), 1)


if __name__ == '__main__':
    unittest.main()