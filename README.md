This repository contain code to customize the output from the unittest module.  The altered code is used for examining students on College level in an introduction python course.

`app/exam_test_result.py` - overshadows methods in [unittest.TextTestResult](https://github.com/python/cpython/blob/master/Lib/unittest/runner.py#L29) to customize the output from unittest.

`app/run_tests.py` - Build test suits and runs them.

`test/test_copy_of_unittest.py` - Is a copy of the test file for the sourcecode of unittest. Is used to limit how much we break the original usage of unitest.

`test/test_exam_text_result.py` - Contains tests for the new functionality of the TextTestResult class.

`test/lp1-2019/` - Contains a running example of the exam_test_result.py code. Stand in `.dbwebb` folder and run with `bash correct.bash`.


Using it, create your tests in a file called test_exam.py. Create one TestCase class for each assignment. Classes name should match `.*Test(Assignment[0-9]+)`.
Each class can contain many test functions. Each function need a docstring.
The docstring should start with explaining what is tested. Then there are three possible options to add, each on its own line and order is important.
If the student function is called with and argument it can be added to the fail output with `{arguments}` in the on a line in docstring.
On next line we can add `{correct}` to show the expected answer.
And on last line should be `{student}` to show what was returned from students function.

Example below.
```
"""
Testar med tom lista
Följande användes som argument till funktionen: {arguments}
Testet förväntar sig att följande lista returneras: {correct}
Följande lista returnerades istället:  {student}
"""
```

In test functions where functions that are tested need arguments, before asserting the function add the arguments as instance member. If there only is one argument add it to `self._argument` and if multiple arguments add them in a list to `self._mult_arguments`.

Example of a TestCase for one assignment:

```
class TestAssignment3(unittest.TestCase):
    """
    Each assignment has 3 testcase with multiple asserts.
    """
    def test_a_valid_isbn(self):
        """
        Test Testar olika korrekta isbn nummer.
        Följande användes som argument till funktionen: {arguments}
        Testet förväntar sig att följande returneras: True
        Följande värde returnerades istället:  {student}
        """
        self._argument = "9781861972712"
        self.assertTrue(exam.validate_isbn(self._argument))
        self._argument = "9781617294136"
        self.assertTrue(exam.validate_isbn(self._argument))
```

# TODO:
- [ ] Try `_mult_arguments`.
- [ ] Write tests
- [ ] Add CircleCi
- [ ] Don't show same error, from different tests for same error.
- [ ] Package so students also get colorama module
    - Install colorama on stud servern? Correct is always run on studeserver. Like validate and inspect?
- [ ] Try removing escaped newlines from output so CONTACT_ERROR_MSG is displayed correctly for all errors.
    - Identify errors where this happens.
- [ ] Add help text for common errors, such as too many inputs when mocking.
- [ ] Remake flowchart as sequence diagram.
- [x] Test it for multiple python versions (Tox?)
- [X] Create custom exception for contacting responsible.
- [x] How to handle "empty" exam.py/functions the students haven't started on?
- [x] Asserts where arguments are on multiple lines destroy the regex for finding assert type. The function call is omitted from error lines. One fix is to overload all assert mehtods in the TestCase class. And save arguments and assert type from there.
- [x] Fix import structure, now we cant run from correct.bash and unittest with same import of files.



# Flowchart of unittest execution

[unittest execution order](https://app.lucidchart.com/invitations/accept/f9604303-3cf8-4cbf-ab22-be0e64b99f49)
