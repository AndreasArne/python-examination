"""
Custom unittest.TextTestResult class. Is used to customize the output from unittests.
"""
import sys
import traceback
import re
from unittest.result import failfast
from unittest.runner import TextTestResult
from colorama import init, Fore, Back, Style

init(strip=False)

STDOUT_LINE = '\nStdout:\n%s'
STDERR_LINE = '\nStderr:\n%s'
CONTACT_ERROR_MSG = (
    Fore.RED + "\n*********\n"
    "Assert method is not ovveriden!\n"
    "Is needed to set answers."
    "\n*********" + Style.RESET_ALL
)

class ExamTestResult(TextTestResult):
    """
    Implementation of TextTestResult to use MyTestResult to create custom output for tests.
    """
    ASSIGNMENT_REGEX = r".*Test(Assignment[0-9]+)\)"
    TEST_NAME_REGEX = r"test_[a-z]_(\w+) "
    ASSERT_TYPE_REGEX = r"self.(assert[A-Z][A-z]+)\("
    ASSERT_ANSWERS_REGEX = {
        "assertTrue": "(.+) is not (.+)",
        "assertFalse": "(.+) is not (.+)",
        "assertEqual": r"^(.+) != (.+)",
        "Lists differ": r"Lists differ: (\[.*\]) != (\[.*\])\n",
        "assertIn": r"(.*) not found in (.*)",
    }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignments_results = {}



    def _exc_info_to_string(self, err, test):
        """
        Converts a sys.exc_info()-style tuple of values into a string.
        Creates custom msg for assertErrors, for the students.
        Code is copied from baseclass and then changed/added to.
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

        #----------------------
        # here starts the interesting code, which we changed. If test failed
        # because of wrong answer from student
        if exctype is test.failureException:
            # student_ans, correct_ans = self.extract_answers_from_different_assert_msgs(value, msgLines)
            function_args = self.get_function_args(test)
            msgLines = self.create_fail_msg(
                function_args,
                test
            )
        #---------------------

        if self.buffer:
            # Dont care about this code
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



    def get_function_args(self, test):
        """
        Use repr() on arguments used for the students defined function.
        If no arguments is used, return None.
        """
        try:
            return repr(getattr(test, "_argument"))
        except AttributeError:
            try:
                return ", ".join([repr(arg) for arg in getattr(test, "_mult_arguments")])
            except AttributeError:
                return None



    def extract_answers_from_different_assert_msgs(self, value, msgLines):
        """
        Try to extract the students answer and the correct answer from fail error.
        """
        try:
            if "AssertionError: Lists differ:" in msgLines[2]:
                # assertEqual with lists need special pattern
                list_diff_group = re.search(self.ASSERT_ANSWERS_REGEX["Lists differ"], msgLines[2])
                student_ans = list_diff_group.group(1)
                correct_ans = list_diff_group.group(2)
            elif "AssertionError: unexpectedly None" in msgLines[2]:
                # assertIsNotNone
                student_ans = "None"
                correct_ans = "Vad som helst förutom None."
            elif "' not found in '" in msgLines[2]:
                # for assertIn, it has switch which group has stud_ans and which has correct_ans
                diff_group = re.search(self.ASSERT_ANSWERS_REGEX["assertIn"], value.args[0].split("\n")[0])
                student_ans = diff_group.group(2)
                correct_ans = diff_group.group(1)
            else:
                assert_type = re.search(self.ASSERT_TYPE_REGEX, msgLines[1]).group(1)
                diff_group = re.search(self.ASSERT_ANSWERS_REGEX[assert_type], value.args[0].split("\n")[0])
                student_ans = diff_group.group(1)
                correct_ans = diff_group.group(2)
        except KeyError as e:
            raise type(e)(str(e) + msgLines[2])\
                .with_traceback(sys.exc_info()[2])
        return student_ans, correct_ans



    def create_fail_msg(self, function_args, test):
        """
        Create formated fail msg using docstring from test function
        """
        #pylint: disable=protected-access
        if test._testMethodDoc is None:
            raise ValueError("Missing docstring. Used for explaining the test when Something is wrong.")
        docstring = re.sub("\n +", "\n", test._testMethodDoc)
        msg_list = docstring.split("\n")
        msg_list[-3] = Back.BLACK + Fore.GREEN + Style.BRIGHT + msg_list[-3] + Style.RESET_ALL
        msg_list[-2] = Back.BLACK + Fore.RED + Style.BRIGHT + msg_list[-2] + Style.RESET_ALL
        msg = "\n".join(msg_list)
        # print(msg_list[-1])
        try:
            return [msg.format(
                arguments=function_args,
                correct=test.correct_answer,
                student=test.student_answer
            )]
        except AttributeError as e:
            raise type(e)(str(e) + CONTACT_ERROR_MSG)\
            .with_traceback(sys.exc_info()[2])
        #pylint: enable=protected-access



    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        if self.errors:
            self.printErrorListWithExplenation("Error", self.errors, "Your code crasched!")
        if self.failures:
            self.printErrorListWithExplenation("Fail", self.failures, "Your code produced wrong result!")



    def printErrorListWithExplenation(self, flavour, errors, explenation):
        """
        Print errors grouped by assignment (TestCase object)
        """
        printed_assignments = []

        self.stream.writeln(self.separator1)
        self.stream.writeln("{} section: {}".format(flavour.upper(), explenation))
        self.stream.writeln(self.separator1)
        for test, err in errors:
            if not test.result_assignment in printed_assignments:
                self.stream.writeln("{}{}s for {}{}".format(
                    Back.MAGENTA + Fore.WHITE,
                    flavour,
                    test.result_assignment,
                    Style.RESET_ALL
                ))
                printed_assignments.append(test.result_assignment)
            for line in err.strip().split("\n"):
                self.stream.writeln("    |" + line)
            self.stream.writeln("    "  + Style.BRIGHT + self.separator2 + Style.RESET_ALL)



    def set_test_name_and_assignment(self, test):
        """
        Extract Assignment from TestCase name.
        Extract test name from test function name.
        Format testname and assignment text and assign to test object.
        """
        test_string = str(test)
        try:
            test.result_assignment = re.search(self.ASSIGNMENT_REGEX, test_string).group(1)
        except AttributeError:
            raise ValueError("Class name for TestCase should the follow structure 'TestAssignment<number>'")

        try:
            test.result_test_name = re.search(self.TEST_NAME_REGEX, test_string).group(1).replace("_", " ")
        except AttributeError:
            raise ValueError("Test function name should follow the structure 'test_<letter>_<name>'")



    def startTestBase(self):
        """
        Base version of startTest, from unittest.TestResult.
        Super() calls the class inbetween this one and TestResult.
        """
        self.testsRun += 1
        self._mirrorOutput = False
        self._setupStdout()



    def startTest(self, test):
        """
        Summary print at beginning of output.
        Group output by Assignment.
        Counts number of tests run for each assignment.
        """
        self.set_test_name_and_assignment(test)
        if not test.result_assignment in self.assignments_results:
            self.assignments_results[test.result_assignment] = {
                "started": 0,
                "success": 0,
            }
            self.stream.write(test.result_assignment + "\n")

        self.assignments_results[test.result_assignment]["started"] += 1

        self.startTestBase()

        MAX_TEST_FUNCNAME_LEN = 25
        TEST_INDENT = 4

        indent = " " * TEST_INDENT
        whitespace = "." * (MAX_TEST_FUNCNAME_LEN - len(test.result_test_name))
        self.stream.write(indent + test.result_test_name + whitespace)
        self.stream.write("... ")
        self.stream.flush()



    def error_is_missing_assignment_function(self, error):
        """
        Returns True if the error is a missing assignment function in the
        students code.
        """
        _, value, tb = error
        if "module 'exam' has no attribute" in str(value):
            while tb.tb_next:
                tb = tb.tb_next
            filename = tb.tb_frame.f_code.co_filename.split("/")[-1]
            if filename == "test_exam.py":
                return True
        return False



    @failfast
    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        if self.error_is_missing_assignment_function(err):
            self.stream.writeln("Assignment Not Implemented")
            return
        self.errors.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True
        self.stream.writeln("ERROR")



    def addSuccess(self, test):
        """
        Counts number of successfull run test for each assignment
        """
        super().addSuccess(test)
        self.assignments_results[test.result_assignment]["success"] += 1
