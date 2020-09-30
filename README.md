This repository contain code to customize the output from the unittest module.  The altered code is used for examining students on College level in an introduction python course.

`app/exam_test_result.py` - overshadows methods in [unittest.TextTestResult](https://github.com/python/cpython/blob/master/Lib/unittest/runner.py#L29) to customize the output from unittest.

`app/run_tests.py` - Build test suits and runs them.

`test/test_copy_of_unittest.py` - Is a copy of the test file for the sourcecode of unittest. Is used to limit how much we break the original usage of unitest.

`test/test_exam_text_result.py` - Contains tests for the new functionality of the TextTestResult class.

`test/lp1-2019/` - Contains a running example of the exam_test_result.py code. Stand in `.dbwebb` folder and run with `bash correct.bash`.




Using it, create your tests in a file called test_exam.py. Create one TestCase class for each assignment. Classes name should match `.*Test[0-9]([A-Z].+)`.
The integer is used to sort the output. Each class can contain many test functions. Each function need a docstring.

Use the docstring to explain what is tested. The docstring is used to display info to the student when their answer is wrong. The output of docstring can be enhanced and display what was used as argument, `{argument}`, to the students function, what the function returned, `{student}`, and what the correct answer is, `{correct}`. It is also possible to inject colors in the output.

By default the line above `{correct}` is colored green and the line above `{student}` is colored red. Manual colors can be injected with `"|<color letter>|"` and reset value `"|/RE|"`. The reset color removes all color options up to that point. The module [colorama](https://pypi.org/project/colorama/) is used for coloring.

Available colors and letters are:

```
"G": Fore.GREEN,
"B": Fore.BLACK,
"R": Fore.RED,
"G": Fore.GREEN,
"Y": Fore.YELLOW,
"BL": Fore.BLUE,
"M": Fore.MAGENTA,
"C": Fore.CYAN,
"W": Fore.WHITE,
"RE": Fore.RESET,
```

Example:
```
"""
|Y|Testar med tom lista|/RE|
Följande användes som argument till funktionen: {arguments}
Testet förväntar sig att följande lista returneras:
{correct}
Följande lista returnerades istället:
{student}
"""
```

In test functions where functions that are tested need arguments, before asserting the function add the arguments as instance member. If there only is one argument add it to `self._argument` and if multiple arguments add them in a list to `self._mult_arguments`.

Example of a TestCase for one assignment:

```
class Test3Assignment3(ExamTestCase):
    """
    Each assignment has 3 testcase with multiple asserts.
    """
    def test_a_valid_isbn(self):
        """
        |M|Test Testar olika korrekta isbn nummer.|/RE|
        Följande användes som argument till funktionen: {arguments}
        Testet förväntar sig att följande returneras: True
        Följande värde returnerades istället:  {student}
        """
        self._argument = "9781861972712"
        self.assertTrue(exam.validate_isbn(self._argument))
        self._argument = "9781617294136"
        self.assertTrue(exam.validate_isbn(self._argument))
```



It is possible to set member `norepr` to True on a testcase. If you don't want `repr()` to be run on the students respons before printing it when a test fail.



# TODO:
- [ ] Change regex for Testcase class name so can have more than "assigment X".
- [ ] Try `_mult_arguments`.
- [ ] Write tests
- [ ] Add CircleCi
- [ ] Package so students also get colorama module
    - Install colorama on stud servern? Correct is always run on studeserver. Like validate and inspect? Or just have coloroama package in .dbwebb folder
- [ ] Add help text for common errors, such as too many inputs when mocking.
- [ ] Try removing escaped newlines from output so CONTACT_ERROR_MSG is displayed correctly for all errors.
    - Identify errors where this happens.
- [ ] Remake flowchart as sequence diagram.
- [x] Don't show same error, from different tests for same error.
- [x] Test it for multiple python versions (Tox?)
- [X] Create custom exception for contacting responsible.
- [x] How to handle "empty" exam.py/functions the students haven't started on?
- [x] Asserts where arguments are on multiple lines destroy the regex for finding assert type. The function call is omitted from error lines. One fix is to overload all assert mehtods in the TestCase class. And save arguments and assert type from there.
- [x] Fix import structure, now we cant run from correct.bash and unittest with same import of files.



# Flowchart of unittest execution

[unittest execution order](https://app.lucidchart.com/invitations/accept/f9604303-3cf8-4cbf-ab22-be0e64b99f49)
