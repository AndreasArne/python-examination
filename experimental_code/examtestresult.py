import traceback
import re
import pdb
from unittest.runner import TextTestResult
from unittest.case import _Outcome
from unittest import TestCase, TestLoader, TestSuite
from operator import itemgetter




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

class ExamTestSuite(TestSuite):


    def __init__(self, tests=[]):
        """
        Makes `_tests` an dict instead of list to force group tests by assignment.
        """
        super().__init__(tests)
        # self._tests = {} # is overritten in super.init(). Used to show intention
        # self._removed_tests = 0
        # self.addTests(tests)



    # def __iter__(self):
    #     sorted_dict = sorted(self._tests.items(), key=itemgetter(0), reverse=True)
    #     tests_sorted = []
    #     print(sorted_dict)
    #     for tup in sorted_dict:
    #         tests_sorted.extend(tup[1])
    #     print(tests_sorted)
    # 
    #     return iter(tests_sorted)



    def addTest(self, test):
        # sanity checks
        if not callable(test):
            raise TypeError("{} is not callable".format(repr(test)))
        if isinstance(test, type) and issubclass(test,
                                                 (case.TestCase, TestSuite)):
            raise TypeError("TestCases and TestSuites must be instantiated "
                            "before passing them to addTest()")
        # kraschar här
        # test blir examtestresult.ExamTestSuite tests=[<__main__.TestAssignment1 testMethod=test_a_text_repetition>]
        # efter att alla tests är tillagda och då funkar det inte
        # if test._assignment in self._tests:
        #     self._tests[test._assignment].append(test)
        # else:
        #     self._tests[test._assignment] = [test]
        self._tests.append(test)


    def addTests(self, tests):
        if isinstance(tests, str):
            raise TypeError("tests must be an iterable of tests, not a string")
        for test in tests:
            # self.set_test_name_and_assignment(test)
            self.addTest(test)
        print(self._tests, "------------------")



    def run(self, result):
        """
        Make sure tests are run in assignment order
        """
        for index, test in enumerate(self):
            if result.shouldStop:
                break
            test(result)
            if self._cleanup:
                self._removeTestAtIndex(index)
        return result

class ExamTestLoader(TestLoader):
    suiteClass = ExamTestSuite



class ExamTestResult(TextTestResult):
    """
    Implementation of TextTestResult to use MyTestResult to create custom output for tests.
    """
    ASSIGNMENT_REGEX = r"\(__main__.Test(.+)\)"
    TEST_NAME_REGEX = r"test_[a-z]_(\w+) "
    ASSERT_TYPE_REGEX = r"self.(assert[A-Z][A-z]+)\("
    ASSERT_ANSWERS_REGEX = {
        "assertTrue": " is not ",
        "assertEqual": r"^(.+) != (.+)",
        "Lists differ": r"Lists differ: (\[.*\]) != (\[.*\])\n",
    }
    ASSIGNEMTS_STARTED = []
    FAULTS = {
        "fails": {},
        "errors": {},
    }
    CONTACT_ERROR_MSG = (
        "\n*********\n"
        "Något gick fel i rättningsprogrammet. "
        "Kontakta Andreas eller Emil med ovanstående felmeddelandet!"
        "\n*********"
    )



    def _exc_info_to_string(self, err, test):
        """
        Converts a sys.exc_info()-style tuple of values into a string.
        Creates custom msg for assertErrors, for the students.
        TO-DO:
        - Lägg till hjälp text för kända fel. T.ex. för felet när man har för många input
        """
        exctype, value, tb = err
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next

        if exctype is test.failureException:
            # Skip assert*() traceback levels
            length = self._count_relevant_tb_levels(tb)
            # length = None
        else:
            length = None
        tb_e = traceback.TracebackException(
            exctype, value, tb, limit=length, capture_locals=self.tb_locals)
        msgLines = list(tb_e.format())

        if exctype is test.failureException:
            try:
                student_ans, correct_ans = self.extract_answers(value, msgLines)
                msgLines = self.create_fail_msg(student_ans, correct_ans, test)
            except Exception as e:
                import sys
                raise type(e)(str(e) + self.CONTACT_ERROR_MSG)\
                    .with_traceback(sys.exc_info()[2])
                
        if self.buffer:
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            if output:
                if not output.endswith('\n'):
                    output += '\n'
                msgLines.append(STDOUT_LINE % output)
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msgLines.append(STDERR_LINE % error)
        return ''.join(msgLines)



    def extract_answers(self, value, msgLines):
        """
        Try to extract the students answer and the correct answer from fail error.
        """
        if "AssertionError: Lists differ:" in msgLines[2]:
            list_diff_group = re.search(self.ASSERT_ANSWERS_REGEX["Lists differ"], msgLines[2])
            student_ans = list_diff_group.group(1)
            correct_ans = list_diff_group.group(2)
        else:
            assert_type = re.search(self.ASSERT_TYPE_REGEX, msgLines[1]).group(1)
            diff_group = re.search(self.ASSERT_ANSWERS_REGEX[assert_type], value.args[0].split("\n")[0])
            student_ans = diff_group.group(1)
            correct_ans = diff_group.group(2)
                
        # print(student_ans)
        # print(correct_ans)
        return student_ans, correct_ans



    def create_fail_msg(self, student_ans, correct_ans, test):
        """
        Create formated fail msg using test functions docstring
        """
        docstring = re.sub("\n +","\n",test._testMethodDoc)
        return [docstring.format(
            correct=correct_ans,
            student=student_ans
        )]



    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList("Error", self.errors)
        self.printErrorList("Fail", self.failures)



    def printErrorList(self, flavour, errors):
        """
        Print errors grouped by assignment (TestCase object)
        TO-DO:
        - visa inte samma error flera gånger, samma fel genereras av varje test funktion
        """
        printed_assignments = []

        self.stream.writeln(self.separator1)
        self.stream.writeln("{} section:".format(flavour.upper()))
        self.stream.writeln(self.separator1)
        for test, err in errors:
            if not test._assignment in printed_assignments:
                self.stream.writeln("{}s for {}".format(flavour, test._assignment))
                printed_assignments.append(test._assignment)
            for line in err.strip().split("\n"):
                self.stream.writeln("    |" + line)
            self.stream.writeln("    " + self.separator2)



    def set_test_name_and_assignment(self, test):
        """
        Set formated testname and assignment text
        """
        test_string = str(test)
        test._assignment = re.search(self.ASSIGNMENT_REGEX, test_string).group(1)
        test._test_name = re.search(self.TEST_NAME_REGEX, test_string).group(1).replace("_", " ")



    def startTest(self, test):
        """
        Group output by Assignment
        """
        super(TextTestResult, self).startTest(test)
        MAX_TEST_FUNCNAME_LEN = 20
        TEST_INDENT = 4
        if self.showAll:
            # desc = self.getDescription(test)
            self.set_test_name_and_assignment(test)
            if not test._assignment in self.ASSIGNEMTS_STARTED:
                self.ASSIGNEMTS_STARTED.append(test._assignment)
                self.stream.write(test._assignment + "\n")

            indent = " " * TEST_INDENT
            whitespace = "." * (MAX_TEST_FUNCNAME_LEN - len(test._test_name))
            self.stream.write(indent + test._test_name + whitespace)
            self.stream.write("... ")
            self.stream.flush()



    def run(self, test):
        "Run the given test case or test suite."
        exit()
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
        if hasattr(result, 'separator1'):
            self.stream.writeln(result.separator1)
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
