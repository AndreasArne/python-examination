"""
pass
"""
import re
from colorama import init, Fore, Back, Style

init(strip=False)



def create_fail_msg(function_args, test):
    """
    Create formated fail msg using docstring from test function
    """
    #pylint: disable=protected-access
    if test._testMethodDoc is None:
        raise AttributeError("Test is missing docstring."
            " Docstring is needed to explainin the test when Something goes wrong.")
    docstring = re.sub("\n +", "\n", test._testMethodDoc)

    msg_list = docstring.split("\n")
    msg_list[-5] = Back.BLACK + Fore.GREEN + Style.BRIGHT + msg_list[-5] + Style.RESET_ALL
    msg_list[-3] = Back.BLACK + Fore.RED + Style.BRIGHT + msg_list[-3] + Style.RESET_ALL
    msg = "\n".join(msg_list)

    return [msg.format(
        arguments=function_args,
        correct=test.correct_answer,
        student=test.student_answer
    )]
    #pylint: enable=protected-access



def get_function_args(test):
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



def error_is_missing_assignment_function(error):
    """
    Returns True if the error is missing function for an assignment in the
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
