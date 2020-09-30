"""
Custom exceptions
"""
from colorama import init, Fore, Style
init(strip=False)

class ExamException(Exception):
    """
    Base exception for custom exception
    """
    pass



class TestFuncNameError(Exception):
    """
    Error for when test function name is wrong
    """
    pass



class TestClassNameError(Exception):
    """
    Error for when test class name is wrong
    """
    pass



class ContanctError(ExamException):
    """
    Custom error. Used when there is an error in the test code and the
    student should contact the person responsible for the exam.
    """
    DEFAULT_MSG = (
        Fore.RED + "\n*********\n"
        "Något gick fel i rättningsprogrammet. "
        "Kontakta Ansvarig med ovanstående felmeddelandet!"
        "\n*********" + Style.RESET_ALL
    )

    def __init__(self, message=DEFAULT_MSG):
        self.message = message
        super().__init__(self.message)
