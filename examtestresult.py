import traceback
import re
from unittest.runner import TextTestResult
from unittest import TestCase
from unittest.case import _Outcome

class ExamTestCase(TestCase):
    def run(self, result=None):
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
            getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, self, skip_why)
            finally:
                result.stopTest(self)
            return
        expecting_failure_method = getattr(testMethod,
                                           "__unittest_expecting_failure__", False)
        expecting_failure_class = getattr(self,
                                          "__unittest_expecting_failure__", False)
        expecting_failure = expecting_failure_class or expecting_failure_method
        outcome = _Outcome(result)
        
        try:
            self._outcome = outcome

            with outcome.testPartExecutor(self):
                self._callSetUp()
            if outcome.success:
                outcome.expecting_failure = expecting_failure
                with outcome.testPartExecutor(self, isTest=True):
                    self._callTestMethod(testMethod)
                outcome.expecting_failure = False
                with outcome.testPartExecutor(self):
                    self._callTearDown()

            self.doCleanups()
            for test, reason in outcome.skipped:
                self._addSkip(result, test, reason)
            self._feedErrorsToResult(result, outcome.errors)
            if outcome.success:
                if expecting_failure:
                    if outcome.expectedFailure:
                        self._addExpectedFailure(result, outcome.expectedFailure)
                    else:
                        self._addUnexpectedSuccess(result)
                else:
                    result.addSuccess(self)
            return result
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

            # explicitly break reference cycles:
            # outcome.errors -> frame -> outcome -> outcome.errors
            # outcome.expectedFailure -> frame -> outcome -> outcome.expectedFailure
            outcome.errors.clear()
            outcome.expectedFailure = None

            # clear the outcome, no more needed
            self._outcome = None
            
class ExamTestResult(TextTestResult):
    """
    Implementation of TextTestResult to use MyTestResult to create custom output for tests.
    """

    ASSIGNMENT_REGEXP = r"\(__main__.Test(.+)\)"
    TEST_NAME_REGEXP = r"test_[a-z]_(\w+) "
    ASSIGNEMTS_STARTED = []

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
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
        self.printErrorList('ERROR', self.errors)
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


    def startTest(self, test):
        """
        Group output by Assignment
        """
        super(TextTestResult, self).startTest(test)
        if self.showAll:
            desc = self.getDescription(test)
            assignment = re.search(self.ASSIGNMENT_REGEXP, desc).group(1)
            test_name = re.search(self.TEST_NAME_REGEXP, desc).group(1).replace("_", " ")
            test.assignment = assignment
            test.test_name = test_name
            if not assignment in self.ASSIGNEMTS_STARTED:
                self.ASSIGNEMTS_STARTED.append(assignment)
                self.stream.write(assignment + "\n")
            indent = " " * 4
            self.stream.write(indent + test_name)
            self.stream.write(" ... ")
            self.stream.flush()
        
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