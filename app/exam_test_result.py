import traceback
import re
from unittest.runner import TextTestResult
from colorama import init
init()
from colorama import Fore, Back, Style
# import pprint
# pp = pprint.PrettyPrinter(indent=4)

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
        "Kontakta Andreas med ovanstående felmeddelandet!"
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

        # here starts the interesting code, which we changed
        if exctype is test.failureException:
            try:
                student_ans, correct_ans = self.extract_answers(value, msgLines)
                function_args = self.extract_function_args(msgLines)
                msgLines = self.create_fail_msg(
                    student_ans,
                    correct_ans,
                    function_args,
                    test
                )
            except Exception as e:
                # Something went wrong in our code
                import sys
                raise type(e)(str(e) + self.CONTACT_ERROR_MSG)\
                    .with_traceback(sys.exc_info()[2])

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



    def extract_function_args(self, msgLines):
        """
        Asserts are done with a function call or a variable, with the students answer.
        Try to get the value that was used as argument for the students function, that is tested.
        TODO:
            - Testa med funktion som tar två arg
            - Testa med funktion som tar två arg, där båda är tupler
        """
        whole_line = msgLines[1]
        try:
            res = re.search("self.assert[A-z]+\(exam.[A-z0-9_]+\((.+)\), ", whole_line)
            return res.group(1)
        except AttributeError:
            # print("No match for function argument!")
            return None


    def extract_answers(self, value, msgLines):
        """
        Try to extract the students answer and the correct answer from fail error.
        """
        try:
            if "AssertionError: Lists differ:" in msgLines[2]:
                list_diff_group = re.search(self.ASSERT_ANSWERS_REGEX["Lists differ"], msgLines[2])
                student_ans = list_diff_group.group(1)
                correct_ans = list_diff_group.group(2)
            else:
                assert_type = re.search(self.ASSERT_TYPE_REGEX, msgLines[1]).group(1)
                diff_group = re.search(self.ASSERT_ANSWERS_REGEX[assert_type], value.args[0].split("\n")[0])
                student_ans = diff_group.group(1)
                correct_ans = diff_group.group(2)
        except AttributeError:
            student_ans = None
            correct_ans = None
        # print(student_ans)
        # print(correct_ans)
        return student_ans, correct_ans



    def create_fail_msg(self, student_ans, correct_ans, function_args, test):
        """
        Create formated fail msg using docstring from test function
        """
        if test._testMethodDoc is None:
            raise ValueError("Missing docstring. Used for explaining the test when Something wrong happens.")
        docstring = re.sub("\n +","\n",test._testMethodDoc)
        msg_list = docstring.split("\n")
        msg_list[-2] = Back.RED + Style.BRIGHT + msg_list[-2] + Style.RESET_ALL
        msg = "\n".join(msg_list)
        # print(msg_list[-1])
        return [msg.format(
            arguments=function_args,
            correct=correct_ans,
            student=student_ans
        )]



    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        if self.errors:
            self.printErrorList("Error", self.errors, "Your code crasched!")
        if self.failures:
            self.printErrorList("Fail", self.failures, "Your code produced wrong result!")



    def printErrorList(self, flavour, errors, explenation):
        """
        Print errors grouped by assignment (TestCase object)
        TO-DO:
        - visa inte samma error flera gånger, samma fel genereras av varje test funktion
        """
        printed_assignments = []

        self.stream.writeln(self.separator1)
        self.stream.writeln("{} section: {}".format(flavour.upper(), explenation))
        self.stream.writeln(self.separator1)
        for test, err in errors:
            if not test._assignment in printed_assignments:
                self.stream.writeln("{}{}s for {}{}".format(
                    Back.MAGENTA + Style.BRIGHT,
                    flavour,
                    test._assignment,
                    Style.RESET_ALL
                ))
                printed_assignments.append(test._assignment)
            for line in err.strip().split("\n"):
                self.stream.writeln("    |" + line)
            self.stream.writeln("    "  + Fore.YELLOW + Style.BRIGHT + self.separator2 + Style.RESET_ALL)



    def set_test_name_and_assignment(self, test):
        """
        Extract Assignment from TestCase name.
        Extract test name from test function name.
        Format testname and assignment text and assign to test object.
        """
        test_string = str(test)
        try:
            test._assignment = re.search(self.ASSIGNMENT_REGEX, test_string).group(1)
        except AttributeError:
            raise ValueError("Class name for TestCase should the follow structure 'TestAssignment<number>'")

        try:
            test._test_name = re.search(self.TEST_NAME_REGEX, test_string).group(1).replace("_", " ")
        except AttributeError:
            raise ValueError("Test function name should follow the structure 'test_<letter>_<name>'")



    def startTest(self, test):
        """
        Summary print at beginning of output.
        Group output by Assignment.
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
