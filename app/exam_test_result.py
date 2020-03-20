import traceback
import re
from unittest.runner import TextTestResult



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
                self.stream.write(test._assignment + "\n--")

            indent = " " * TEST_INDENT
            whitespace = "." * (MAX_TEST_FUNCNAME_LEN - len(test._test_name))
            self.stream.write(indent + test._test_name + whitespace)
            self.stream.write("... ")
            self.stream.flush()



    # def run(self, test):
    #     "Run the given test case or test suite."
    #     exit()
    #     result = self._makeResult()
    #     registerResult(result)
    #     result.failfast = self.failfast
    #     result.buffer = self.buffer
    #     result.tb_locals = self.tb_locals
    #     with warnings.catch_warnings():
    #         if self.warnings:
    #             # if self.warnings is set, use it to filter all the warnings
    #             warnings.simplefilter(self.warnings)
    #             # if the filter is 'default' or 'always', special-case the
    #             # warnings from the deprecated unittest methods to show them
    #             # no more than once per module, because they can be fairly
    #             # noisy.  The -Wd and -Wa flags can be used to bypass this
    #             # only when self.warnings is None.
    #             if self.warnings in ['default', 'always']:
    #                 warnings.filterwarnings('module',
    #                         category=DeprecationWarning,
    #                         message=r'Please use assert\w+ instead.')
    #         startTime = time.perf_counter()
    #         startTestRun = getattr(result, 'startTestRun', None)
    #         if startTestRun is not None:
    #             startTestRun()
    #         try:
    #             test(result)
    #         finally:
    #             stopTestRun = getattr(result, 'stopTestRun', None)
    #             if stopTestRun is not None:
    #                 stopTestRun()
    #         stopTime = time.perf_counter()
    #     timeTaken = stopTime - startTime
    #     result.printErrors()
    #     if hasattr(result, 'separator1'):
    #         self.stream.writeln(result.separator1)
    #     run = result.testsRun
    #     self.stream.writeln("Ran %d test%s in %.3fs" %
    #                         (run, run != 1 and "s" or "", timeTaken))
    #     self.stream.writeln()
    # 
    #     expectedFails = unexpectedSuccesses = skipped = 0
    #     try:
    #         results = map(len, (result.expectedFailures,
    #                             result.unexpectedSuccesses,
    #                             result.skipped))
    #     except AttributeError:
    #         pass
    #     else:
    #         expectedFails, unexpectedSuccesses, skipped = results
    # 
    #     infos = []
    #     if not result.wasSuccessful():
    #         self.stream.write("FAILED")
    #         failed, errored = len(result.failures), len(result.errors)
    #         if failed:
    #             infos.append("failures=%d" % failed)
    #         if errored:
    #             infos.append("errors=%d" % errored)
    #     else:
    #         self.stream.write("OK")
    #     if skipped:
    #         infos.append("skipped=%d" % skipped)
    #     if expectedFails:
    #         infos.append("expected failures=%d" % expectedFails)
    #     if unexpectedSuccesses:
    #         infos.append("unexpected successes=%d" % unexpectedSuccesses)
    #     if infos:
    #         self.stream.writeln(" (%s)" % (", ".join(infos),))
    #     else:
    #         self.stream.write("\n")
    #     return
