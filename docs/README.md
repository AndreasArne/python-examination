Examiner is a layer on top of pythons unittest framwork, for more verbose and clear output when test fail. It is used in a university course to examinate student in a introductionary python course. 

You can see working examples of it in `test/analyzer/.dbwebb`. To run it you first need to build it, run `make build`, it will copy external modules into the package so it can be distributed to students. Then you can find the folder `examiner` in the build folder. Execute `bash correct.bash` in `test/analyzer/.dbwebb`, it will copy the package. to run it.

Examiner utilize function docstrings for testcases to modify and specialize error outputs for each test.

So far it only supports tests in one file, `test_exam.py`. TestCase classes need to inherit from `ExamTestCase` and naming should follow the regex `.*Test[0-9]([A-Z].+)`. The number is used to sort execution order and the output.


Test function need to follow the naming, `"test_[a-z]_(\w+)"`, and have a docstring. The docstring is used when test fail. The output of docstring can be enhanced and display what was used as argument, `{argument}`, to the students function, what the function returned, `{student}`, and what the correct answer is, `{correct}`. It is also possible to inject colors in the output.

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
- [ ] Try `_mult_arguments`.
- [ ] Write tests
- [ ] Add CircleCi
    - Install colorama on stud servern? Correct is always run on studeserver. Like validate and inspect? Or just have coloroama package in .dbwebb folder
- [ ] Add help text for common errors, such as too many inputs when mocking.
- [ ] Try removing escaped newlines from output so CONTACT_ERROR_MSG is displayed correctly for all errors.
    - Identify errors where this happens.
- [ ] Remake flowchart as sequence diagram.
- [x] Package so students also get colorama module
- [x] Change regex for Testcase class name so can have more than "assigment X".
- [x] Don't show same error, from different tests for same error.
- [x] Test it for multiple python versions (Tox?)
- [X] Create custom exception for contacting responsible.
- [x] How to handle "empty" exam.py/functions the students haven't started on?
- [x] Asserts where arguments are on multiple lines destroy the regex for finding assert type. The function call is omitted from error lines. One fix is to overload all assert mehtods in the TestCase class. And save arguments and assert type from there.
- [x] Fix import structure, now we cant run from correct.bash and unittest with same import of files.



# Flowchart of unittest execution

[unittest execution order](https://app.lucidchart.com/invitations/accept/f9604303-3cf8-4cbf-ab22-be0e64b99f49)
