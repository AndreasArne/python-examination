import unittest
import traceback
from unittest import TextTestRunner
from unittest.runner import TextTestResult


"""
https://stackoverflow.com/questions/26044977/python-3-unittest-how-to-extract-results-of-tests
https://github.com/python/cpython/tree/master/Lib/unittest
"""



class MyTextTestResult(TextTestResult):
    """
    Implementation of TextTestResult to use MyTestResult to create custom output for tests.
    """
    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        # print(exctype, value, tb)
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next

        if exctype is test.failureException:
            # AssertionErrors (FAIL)
            # Skip assert*() traceback levels
            # length = self._count_relevant_tb_levels(tb)
            # print(dir(test))
            msg = " ".join(test._testMethodName.split("_")[2:])
            msg += "|" + test._testMethodDoc.strip()
            # print("*****************")
            # print(msg)
            # print(test._testMethodDoc.strip())
            # print("*****************")
            msgLines = [msg]
        else:
            # Other Errors (ERROR)
            length = None
            tb_e = traceback.TracebackException(
                exctype, value, tb, limit=length, capture_locals=self.tb_locals)
            msgLines = list(tb_e.format())

        # if self.buffer:
        #     print("HERE====================================")
        #     output = sys.stdout.getvalue()
        #     error = sys.stderr.getvalue()
        #     if output:
        #         if not output.endswith('\n'):
        #             output += '\n'
        #         msgLines.append(STDOUT_LINE % output)
        #     if error:
        #         if not error.endswith('\n'):
        #             error += '\n'
        #         msgLines.append(STDERR_LINE % error)
        # return "msg line"
        return ''.join(msgLines)
    
    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        # self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        """
        flavour == "Fail" or "Error"
        """
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings('module',
                            category=DeprecationWarning,
                            message=r'Please use assert\w+ instead.')
            startTime = time.perf_counter()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
            try:
                test(result)
            finally:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            stopTime = time.perf_counter()
        timeTaken = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            self.stream.write("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        return

class TestFunc(unittest.TestCase):

    def test_a_pass(self):
            self.assertEqual(1, 1)

    
    def test_b_error(self):
        h = 1
        "hej" - h
        self.assertIsNotNone(1)

    
    def test_c_uppgift_3(self):
        """
        Du har fel på uppgift 3 i testet som kollar att input 2 till funktionen ger output 0.
        """
        self.assertTrue(0)

if __name__ == '__main__':
    runner = TextTestRunner(resultclass=MyTextTestResult, verbosity=3)
    unittest.main(testRunner=runner)