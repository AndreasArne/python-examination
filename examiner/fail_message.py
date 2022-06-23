"""
Contains class for creating the fail message list when a test fails och crash
"""
import re
import examiner.helper_functions as hf

try:
    from examiner.colorama import init, Fore, Back, Style
except ImportError:
    from colorama import init, Fore, Back, Style

init(strip=False)

class FailMessage():
    """
    Used to create fail message list
    """
    def __init__(self, methodDoc):
        #pylint: disable=protected-access
        if methodDoc is None:
            raise AttributeError(
                "Test is missing docstring."
                " Docstring is needed to explainin the test when Something goes wrong."
            )
        self.docstring = re.sub("\n +", "\n", methodDoc)
        #pylint: enable=protected-access

        self.arguments = None
        self.student_answer = ""
        self.correct_answer = ""
        self.norepr = False


    def set_answers(self, student_answer, correct_answer):
        """
        Set students answer and correct answer as members.
        """
        self.student_answer = repr(student_answer)
        self.correct_answer = repr(correct_answer)
        if self.norepr:
            if isinstance(student_answer, str):
                self.student_answer = hf.clean_str(student_answer)
            else:
                self.student_answer = str(student_answer)



    def create_fail_msg(self, traceback=None):
        """
        Create formated fail msg using docstring from test function
        """
        msg_list = self.docstring.split("\n")
        self.inject_answer_colors(msg_list)
        msg = "\n".join(msg_list)
        msg = self.inject_regex_colors(msg)

        return [msg.format(
            arguments=self.arguments,
            correct=self.correct_answer,
            student=self.student_answer if traceback is None else traceback
        )]



    def get_color_indexes(self, msg_list):
        """
        Return index of lines with {correct} (green) and {student} (red).
        """
        indexes = {}
        for i, line in enumerate(msg_list):
            if "{correct}" in line:
                indexes["green"] = i - 1
            elif "{student}" in line:
                indexes["red"] = i - 1

        return indexes



    def inject_answer_colors(self, msg_list):
        """
        Insert red and green color if "correct" and "student" is present in doscring.
        """
        indexes = self.get_color_indexes(msg_list)
        if "green" in indexes:
            i = indexes["green"]
            msg_list[i] = (
                Back.BLACK + Fore.GREEN + Style.BRIGHT
                + msg_list[i]
                + Style.RESET_ALL
            )
        if "red" in indexes:
            i = indexes["red"]
            msg_list[i] = (
                Back.BLACK + Fore.RED + Style.BRIGHT
                + msg_list[i]
                + Style.RESET_ALL
            )

        return msg_list



    def inject_regex_colors(self, msg):
        """
        Use regex to find |<color letter>| and replace with colors.
        """
        color_start = re.findall(hf.COLOR_REGEX_START, msg)
        for color in color_start:
            msg = msg.replace(f"|{color}|", hf.COLORS[color]+ Style.BRIGHT)
        msg = msg.replace("|/RE|", hf.COLORS["RE"])
        return msg
